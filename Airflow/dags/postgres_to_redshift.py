from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
import csv
from io import StringIO
import boto3
import time
import json

client = boto3.client('redshift-data',region_name='us-east-1')
workgroupName='default-workgroup'
database='dev'
s3_bucket = 'airflow-redshift-usecase'
s3_key = 'staged_data/data.csv'

def create_table_in_redshift():
    
    response = client.execute_statement(
        WorkgroupName=workgroupName, ### Use ClusterIdentifier if not serverless
        Database=database,
        #DbUser='admin', ''' Only with a cluster not serverless '''
        Sql='CREATE TABLE IF NOT EXISTS employees (id VARCHAR (255) NOT NULL, name VARCHAR (255) NOT NULL, time_added TIMESTAMP);'
    )

def extract_data_from_postgres(*args, **kwargs):
    postgres_hook = PostgresHook(postgres_conn_id='my_postgres_cnn')
    #last_modified_date = kwargs['dag_run'].conf.get('last_modified_date')
    #query = f"SELECT * FROM your_table WHERE modified_date > '{last_modified_date}'"
    query = "SELECT * FROM employees"
    records = postgres_hook.get_records(query)
    return records

def load_data_to_redshift(*args, **kwargs):
    records = kwargs['ti'].xcom_pull(task_ids='extract_postgres_data')

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    for record in records:
        csv_writer.writerow(record)

    s3_bucket = 'airflow-redshift-usecase'
    s3_key = 'staged_data/data.csv'
    s3_hook = S3Hook(aws_conn_id='my_aws_cnn')
    s3_hook.load_string(
        string_data=csv_buffer.getvalue(),
        bucket_name=s3_bucket,
        key=s3_key,
        replace=True
    )
    csv_buffer.close()

    # Use boto3 to call Redshift Data API
    response = client.execute_statement(
        WorkgroupName=workgroupName,
        Database=database,
        Sql=f"""
            COPY employees
            FROM 's3://{s3_bucket}/{s3_key}'
            IAM_ROLE 'arn:aws:iam::411616681997:role/AmazonRedshiftServerlessAllCommands' 
            CSV;
        """
    )


default_args={
    'owner': 'me',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    dag_id="postgres_to_redshift",
    description="simple ETL from postgres to redshift",
    schedule_interval=('@once'),
    start_date=days_ago(1),
    tags=['ETL','pipeline','aws','postgres','redshift']
)as dag:
    create_redshift_table=PythonOperator(
        task_id="create_table_in_redshift",
        python_callable=create_table_in_redshift,
        provide_context=True,
        dag=dag
    )

    extract_data=PythonOperator(
        task_id="extract_postgres_data",
        python_callable=extract_data_from_postgres,
        provide_context=True,
        dag=dag
    )
    load_data=PythonOperator(
        task_id="load_to_redshift_table",
        python_callable=load_data_to_redshift,
        provide_context=True,
        dag=dag
    )
    

create_redshift_table >> extract_data >> load_data