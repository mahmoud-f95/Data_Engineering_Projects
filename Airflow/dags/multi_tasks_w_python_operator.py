from airflow import DAG
from airflow.operators.python import PythonOperator
#from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime,timedelta


def greeting(name):
    print(f"Hello {name}!".format(name=name))

def greeting_from(name,place):
    print("Hello {name}!, from {place}".format(name=name,place=place))

def task_c():
    print("Task C executed")

def task_d():
    print("Task D executed")

with DAG(
    dag_id="execute_multiple_python_tasks",
    description="Dag with multiple tasks dependencies with python ops",
    start_date=days_ago(1),
    schedule_interval="@once",
    catchup=False
)as dag:
    taskA=PythonOperator(
        task_id="task_A",
        python_callable=greeting,
        op_kwargs={"name":"Mahmoud"}
    )
    taskB=PythonOperator(
        task_id="task_B",
        python_callable=greeting_from,
        op_kwargs={"name":"Mahmoud","place":"the other side"}
    )
    taskC=PythonOperator(
        task_id="task_C",
        python_callable=task_c
    )
    taskD=PythonOperator(
        task_id="task_D",
        python_callable=task_d,
    )

### Using down/up stream 
"""
    taskA.set_downstream(taskB)
    taskA.set_downstream(taskC)

    taskD.set_upstream(taskB)
    taskD.set_upstream(taskC)
"""

### Using operators

taskA >> [taskB,taskC]
taskD << [taskB,taskC]
