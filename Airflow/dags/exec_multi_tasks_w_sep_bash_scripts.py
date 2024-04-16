from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime,timedelta

with DAG(
    dag_id="execute_multiple_bash_scripts_tasks_",
    description="Dag with multiple tasks dependencies with bash scripts",
    start_date=days_ago(30),
    schedule_interval="0 0,12 * * 0,3",
    template_searchpath="/home/mahmoud/airflow/dags/bash_scripts",
    catchup=True
)as dag:
    taskA=BashOperator(
        task_id="task_A",
        bash_command="task_A.sh",
    )
    taskB=BashOperator(
        task_id="task_B",
        bash_command="task_B.sh",
    )
    taskC=BashOperator(
        task_id="task_C",
        bash_command="task_C.sh",
    )
    taskD=BashOperator(
        task_id="task_D",
        bash_command="task_D.sh",
    )
    taskE=BashOperator(
        task_id="task_E",
        bash_command="task_E.sh",
    )
    taskF=BashOperator(
        task_id="task_F",
        bash_command="task_F.sh",
    )
    taskG=BashOperator(
        task_id="task_G",
        bash_command="task_G.sh",
    )

### Using down/up stream 
"""
    taskA.set_downstream(taskB)
    taskA.set_downstream(taskC)

    taskD.set_upstream(taskB)
    taskD.set_upstream(taskC)
"""

### Using operators

taskA >> taskB >>taskE
taskA >> taskC >> taskF
taskA >> taskD >> taskG
