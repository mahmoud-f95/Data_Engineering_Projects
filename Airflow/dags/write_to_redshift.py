from airflow import DAG
from airflow.providers.amazon.aws.hooks.redshift_sql import RedshiftSQLHook
from airflow.operators.python import PythonOperator 
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
import redshift_connector
import boto3
import time

client = boto3.client('redshift-data', region_name='us-east-1')
workgroupName='default-workgroup'
database='dev'

def create_table_in_redshift():
    
    response = client.execute_statement(
        WorkgroupName=workgroupName, ### Use ClusterIdentifier if not serverless
        Database=database,
        #DbUser='admin', ''' Only with a cluster not serverless '''
        Sql='CREATE TABLE IF NOT EXISTS employees (id VARCHAR (255) NOT NULL, name VARCHAR (255) NOT NULL);'
    )

def insert_data_in_redshift():
    
    response = client.execute_statement(
        WorkgroupName=workgroupName, ### Use ClusterIdentifier if not serverless
        Database=database,
        #DbUser='admin', ''' Only with a cluster not serverless '''
        Sql="""INSERT INTO employees(id,name) VALUES 
        ('1','Ahmed'), 
        ('2','Ali') , 
        ('3','Rami'),
        ('4','Adel');"""
    )

def display_data_in_airflow():
    
    response = client.execute_statement(
        WorkgroupName=workgroupName, ### Use ClusterIdentifier if not serverless
        Database=database,
        #DbUser='admin', ''' Only with a cluster not serverless '''
        Sql="""SELECT * FROM employees;"""
    )
    query_id = response['Id']

    # Wait for the query to finish
    while True:
        status_response = client.describe_statement(Id=query_id)
        status = status_response['Status']
        if status in ['FINISHED', 'FAILED', 'ABORTED']:
            break
        time.sleep(5)  # sleep for 5 seconds before polling again

    # Check if the query was successful
    if status == 'FINISHED':
        # Fetch the result
        result_response = client.get_statement_result(Id=query_id)
        # Process and return the result
        # Note: You need to format the result as per your requirement
        return result_response['Records']
    else:
        raise Exception(f"Query failed with status: {status}")
    

    
    

default_args={
    'owner': 'me',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    dag_id="write_to_redshift",
    description="connect and write to redshift DWH",
    schedule_interval=('@once'),
    start_date=days_ago(1),
    tags=['aws','redshift','DWH']
)as dag:
    create_table=PythonOperator(
        task_id="create_redshift_table",
        python_callable=create_table_in_redshift,
        dag=dag
    )
    populate_table=PythonOperator(
        task_id="populate_redshift_table",
        python_callable=insert_data_in_redshift,
        dag=dag
    )
    display_table=PythonOperator(
        task_id="display_redshift_table",
        python_callable=display_data_in_airflow,
        do_xcom_push=True,
        dag=dag
    )


create_table >> populate_table >>display_table