from airflow import DAG
from airflow.operators.python import PythonOperator
#from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime,timedelta


def increment_1(value):
    print(f"value {value}!".format(value=value))
    return value+1

def multiply_100(ti):
    value=ti.xcom_pull(task_ids="increment_1")
    print("value {value}".format(value=value))
    return value*100

def substruct_9(ti):
    value=ti.xcom_pull(task_ids="multiply_100")
    print("value {value}".format(value=value))
    return value - 9
    
def print_last_value(ti):
    value=ti.xcom_pull(task_ids="substruct_9")
    print("value {value}".format(value=value))

with DAG(
    dag_id="xcom_with_python_operator",
    description="Dag with XCom and python operator",
    start_date=days_ago(1),
    schedule_interval="@once",
    catchup=False
)as dag:
    increment_by_1=PythonOperator(
        task_id="increment_1",
        python_callable=increment_1,
        op_kwargs={"value":1}
    )
    multiply_by_100=PythonOperator(
        task_id="multiply_100",
        python_callable=multiply_100,
    )
    substruct_by_9=PythonOperator(
        task_id="substruct_9",
        python_callable=substruct_9,
    )
    print_current_value=PythonOperator(
        task_id="print_last_value",
        python_callable=print_last_value,
    )

### Using down/up stream 
"""
    taskA.set_downstream(taskB)
    taskA.set_downstream(taskC)

    taskD.set_upstream(taskB)
    taskD.set_upstream(taskC)
"""

### Using operators

increment_by_1 >> multiply_by_100 >> substruct_by_9 >> print_current_value

