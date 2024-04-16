from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta


def hello_world():
    print("Hello World!")

with DAG(
    dag_id="first_dag",
    start_date=datetime(2024,1,14),
    schedule_interval="*/5 * * * *",
    catchup=False
)as dag:
    task1=PythonOperator(
        task_id="print_word",
        python_callable=hello_world
    )


task1