from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago


default_args={
    'owner': 'me',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id="write_to_postgresql",
    description="connect and write to postgresql db",
    schedule_interval=('@once'),
    start_date=days_ago(1),
    tags=['postgres','db_connection','write_to_db']
)as dag:
    create_table=PostgresOperator(
        task_id='create_table',
        postgres_conn_id='my_postgres_cnn',
        sql="""
            CREATE TABLE IF NOT EXISTS employees(
            id SERIAL PRIMARY KEY,
            name VARCHAR (255) NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
        dag=dag,
    )

    insert_values=PostgresOperator(
        task_id='populate_table',
        postgres_conn_id='my_postgres_cnn',
        sql="""
            INSERT INTO employees(id,name) VALUES
            (1,'Ahmed'),
            (2,'Ali') ,
            (3,'Rami'),
            (4,'Adel');
            """,
        dag=dag,
    )

    display_output=PostgresOperator(
        task_id='display_table',
        postgres_conn_id='my_postgres_cnn',
        sql="""
            SELECT * FROM employees;
            """,
        do_xcom_push=True,
        dag=dag,
    )

create_table >> insert_values >> display_output