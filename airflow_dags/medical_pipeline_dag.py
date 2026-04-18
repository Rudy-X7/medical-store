from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2024, 1, 1),
}

with DAG(
    dag_id='medical_store_pipeline',
    schedule_interval='@daily',
    catchup=False,
    default_args=default_args
) as dag:

    generate_data = BashOperator(
        task_id='generate_data',
        bash_command='python3 ~/final_project/scripts/ingestion/generate_data.py'
    )

    clean_data = BashOperator(
        task_id='clean_data',
        bash_command='python3 ~/final_project/scripts/processing/clean_data.py'
    )

    generate_data >> clean_data
