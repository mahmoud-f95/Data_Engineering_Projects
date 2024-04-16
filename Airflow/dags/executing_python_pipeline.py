from airflow import DAG
from airflow.operators.python import PythonOperator
#from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime,timedelta
import pandas as pd
import json

def read_csv():
    df=pd.read_csv("/home/mahmoud/airflow/datasets/insurance.csv")
    print (df)
    return df.to_json()

def remove_nulls(**kwargs):
    ti=kwargs['ti']
    data=ti.xcom_pull(task_ids="read_csv")
    df=pd.read_json(data)
    df=df.dropna()
    print(df)
    return df.to_json()

def group_by_smokers(ti):
    data=ti.xcom_pull(task_ids="remove_nulls")
    df=pd.read_json(data)
    smokers_df=df.groupby('smoker').agg({'age':'mean','bmi':'mean'}).reset_index()
    smokers_df.to_csv('/home/mahmoud/airflow/outputs/pipeline_1/smokers.csv',index=False)


def group_by_region(ti):
    data=ti.xcom_pull(task_ids="remove_nulls")
    df=pd.read_json(data)
    smokers_df=df.groupby('region').agg({'age':'mean','bmi':'mean'}).reset_index()
    smokers_df.to_csv('/home/mahmoud/airflow/outputs/pipeline_1/regions.csv',index=False)



with DAG(
    dag_id="execute_python_pipeline",
    description="Dag with simple python pipeline",
    start_date=days_ago(1),
    schedule_interval="@once",
    catchup=False
)as dag:
    read_csv_file=PythonOperator(
        task_id="read_csv",
        python_callable=read_csv,
    )
    remove_null_values=PythonOperator(
        task_id="remove_nulls",
        python_callable=remove_nulls,
    )
    groupby_smokers=PythonOperator(
        task_id="groupby_smokers",
        python_callable=group_by_smokers,
    )
    groupby_region=PythonOperator(
        task_id="groupby_region",
        python_callable=group_by_region,
    )

    

### Using down/up stream 


### Using operators

read_csv_file >> remove_null_values >> [groupby_smokers,groupby_region]

