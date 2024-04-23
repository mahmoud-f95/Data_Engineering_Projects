from airflow import DAG
from airflow.operators.python import PythonOperator,BranchPythonOperator
#from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
from airflow.utils.edgemodifier import Label
from datetime import datetime,timedelta
import pandas as pd
import json


OUTPUT_PATH='PATH_TO_OUTPUT_FILE'

def read_csv(ti):
    df=pd.read_csv("Datasets/insurance.csv")
    print (df)
    ti.xcom_push(key="dataset",value=df.to_json())
    

def remove_nulls(**kwargs):
    ti=kwargs['ti']
    data=ti.xcom_pull(key="dataset")
    df=pd.read_json(data)
    df=df.dropna()
    print(df)
    ti.xcom_push(key="clean_data",value=df.to_json())

def determining_branch():
    transformation_action=Variable.get('transformation_action',default_var=None)

    ### returning the following task_id based on a condition
    if transformation_action.startswith('filter'):
        return 'Filtering.'+transformation_action
    elif transformation_action =='group_by_region_smokers':
        return 'Grouping.group_by_region_smokers'
    


def group_by_region_smokers(ti):
    data=ti.xcom_pull(key='clean_data')
    df=pd.read_json(data)
    smokers_df=df.groupby('smoker').agg({'age':'mean','bmi':'mean'}).reset_index()
    smokers_df.to_csv(OUTPUT_PATH.format('grouped_by_smokers'),index=False)

    smokers_df=df.groupby('region').agg({'age':'mean','bmi':'mean'}).reset_index()
    smokers_df.to_csv(OUTPUT_PATH.format('grouped_by_region'),index=False)

def filter_by_southeast(ti):
    data=ti.xcom_pull(key='clean_data')
    df=pd.read_json(data)
    df_southeast=df[df['region']=="southeast"]
    df_southeast.to_csv(OUTPUT_PATH.format('southeast'),index=False)


def filter_by_southwest(ti):
    data=ti.xcom_pull(key='clean_data')
    df=pd.read_json(data)
    df_southeast=df[df['region']=="southwest"]
    df_southeast.to_csv(OUTPUT_PATH.format('southwest'),index=False)

def filter_by_northeast(ti):
    data=ti.xcom_pull(key='clean_data')
    df=pd.read_json(data)
    df_southeast=df[df['region']=="northeast"]
    df_southeast.to_csv(OUTPUT_PATH.format('northeast'),index=False)

def filter_by_northwest(ti):
    data=ti.xcom_pull(key='clean_data')
    df=pd.read_json(data)
    df_southeast=df[df['region']=="northwest"]
    df_southeast.to_csv(OUTPUT_PATH.format('northwest'),index=False)



with DAG(
    dag_id="branching_with_variables",
    description="Dag branching with preset variable",
    start_date=days_ago(1),
    schedule_interval="@once",
    tags = ['python', 'transform', 'pipeline', 'branching']
)as dag:
    with TaskGroup('Reading_and_Preprocessing') as reading_and_preprocessing:
        read_csv_file=PythonOperator(
            task_id="read_csv",
            python_callable=read_csv,
        )
        remove_null_values=PythonOperator(
            task_id="remove_nulls",
            python_callable=remove_nulls,
        )

    determining_branch=BranchPythonOperator(
        task_id="determine_branch",
        python_callable=determining_branch,
    )

    with TaskGroup('Grouping') as grouping:
        group_by_region_smokers=PythonOperator(
            task_id="group_by_region_smokers",
            python_callable=group_by_region_smokers,
        )

    with TaskGroup('Filtering') as filtering:
        filter_by_southeast=PythonOperator(
            task_id="filter_by_southeast",
            python_callable=filter_by_southeast,
        )
        filter_by_southwest=PythonOperator(
            task_id="filter_by_southwest",
            python_callable=filter_by_southwest,
        )
        filter_by_northeast=PythonOperator(
            task_id="filter_by_northeast",
            python_callable=filter_by_northeast,
        )
        filter_by_northwest=PythonOperator(
            task_id="filter_by_northwest",
            python_callable=filter_by_northwest,
        )

    

### Using down/up stream 


### Using operators

reading_and_preprocessing >> Label('clean_data') >> determining_branch >> Label('Based on Variable is Branched') >> [filtering,grouping]

