from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime,timedelta

with DAG(
    dag_id="execute_multiple_tasks",
    description="Dag with multiple tasks dependencies",
    start_date=days_ago(1),
    schedule_interval="@once",
    catchup=False
)as dag:
    taskA=BashOperator(
        task_id="task_A",
        bash_command="""echo task A has started
                        for i in {1..10}
                        do 
                            echo task a is printing $i
                        done
                        echo task A has ended
                        """,
    )
    taskB=BashOperator(
        task_id="task_B",
        bash_command="""echo task B has started
                        sleep 4
                        echo task B has ended
                        """,
    )
    taskC=BashOperator(
        task_id="task_C",
        bash_command="""echo task C has started
                        sleep 15
                        echo task C has ended
                        """,
    )
    taskD=BashOperator(
        task_id="task_D",
        bash_command="echo task D now completed",
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
