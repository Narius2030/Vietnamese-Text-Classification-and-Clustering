from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime

import sys
sys.path.append("/mnt/d/Programming/Vietnamese-Text-Generator/airflow/plugins/")
from crawl_news import scrape_news
from clean_data import transform_load

def print_date():
    print('Today is {}'.format(datetime.today().date()))
    
dag = DAG(
    'ETL-VNExpress',
    default_args={'start_date': days_ago(1)},
    schedule_interval='55 17 * * *',
    catchup=False
)

extract_data = PythonOperator(
    task_id='extract_data',
    python_callable=scrape_news,
    dag=dag
)

transform_load = PythonOperator(
    task_id='transform_load',
    python_callable=transform_load,
    dag=dag
)

print_date_task = PythonOperator(
    task_id='print_date',
    python_callable=print_date,
    dag=dag
)


# Set the dependencies between the tasks
extract_data >> transform_load >> print_date_task
# transform_load >> print_date_task