from airflow import DAG

from airflow.providers.sqlite.operators.sqlite import SqliteOperator


from datetime import date, datetime, timedelta
from airflow.utils.dates import days_ago



with DAG(
    dag_id = 'executing_sql_pipeline',
    description = 'Pipeline using SQL operators',
    start_date = days_ago(1),
    schedule_interval = '@once',
    tags = ['pipeline', 'sql']
) as dag:
    create_table = SqliteOperator(
        task_id = 'create_table',
        sql = r"""
            CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    age INTEGER NOT NULL,
                    is_active BOOLEAN DEFAULT true,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        sqlite_conn_id = 'my_sqlite_cnn',
        dag = dag,
    )
    insert_values_1=SqliteOperator(
        task_id="insertion_1",
        sql = r"""
            INSERT INTO users (name, age, is_active) VALUES 
                ('Julie', 30, false),
                ('Peter', 55, true),
                ('Emily', 37, false),
                ('Katrina', 54, false),
                ('Joseph', 27, true);
        """,
        sqlite_conn_id='my_sqlite_cnn',
        dag=dag
    )

    insert_values_2=SqliteOperator(
        task_id="insertion_2",
        sql = r"""
            INSERT INTO users (name, age) VALUES 
                ('Harry', 49),
                ('Nancy', 52),
                ('Elvis', 26),
                ('Mia', 20);
        """,
        sqlite_conn_id='my_sqlite_cnn',
        dag=dag
    )
    display_output=SqliteOperator(
        task_id="output_displaying",
        sql=r"""
        SELECT * FROM users
        """,
        sqlite_conn_id='my_sqlite_cnn',
        dag=dag,
        do_xcom_push=True
    )

create_table >> [insert_values_1 , insert_values_2] >> display_output

