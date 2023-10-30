from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from src.database.database_management import DBManagement
from src.web_srapping.cv_online import CvOnline
from src.web_srapping.cv_market import CvMarket
from src.web_srapping.cv_bankas import CVBankas

default_args = {
    'owner': 'Viktoras',
    'retries': 3,
    'retry_delay': timedelta(minutes=2)
}


def scrap_data_from_cv_online_page():
    """
    Scraps CV Online page
    """
    print('Scrapping cv online page and inserting in DB')
    cv_online = CvOnline(jobs=['data', 'engeeniring'])
    cv_online.run_scrap()
    print('Data injected in DB')


def scrap_data_from_cv_market_page():
    """
    Scraps CV Market page
    """
    print('Scrapping cv online page and inserting in DB')
    cv_market = CvMarket()
    cv_market.run_scrap()
    print('Data injected in DB')


def scrap_data_from_cv_bankas_page():
    """
    Scraps CV Bank page
    """
    print('Scrapping cv online page and inserting in DB')
    cv_bank = CVBankas()
    cv_bank.run_scrap()
    print('Data injected in DB')


def calculate_in_db():
    """
    Calculation in DB
    """
    print('Inserting calculations in jobs_info table')
    db = DBManagement()
    db.add_data_to_jobs_data_table()
    db.close_session()
    print('Data injected in jobs_info table')


with DAG(
    dag_id='python_1',
    default_args=default_args,
    description="Lets try to do something",
    start_date=datetime(2023, 10, 22, 0),
    schedule_interval='@daily',
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id='scrap_data_from_cv_online_page',
        python_callable=scrap_data_from_cv_online_page,
    )

    task2 = PythonOperator(
        task_id='scrap_data_from_cv_market_page',
        python_callable=scrap_data_from_cv_market_page,
    )

    task3 = PythonOperator(
        task_id='scrap_data_from_cv_bankas_page',
        python_callable=scrap_data_from_cv_bankas_page,
    )

    task4 = PythonOperator(
        task_id='calculate_in_db',
        python_callable=calculate_in_db,
    )

    [task1, task2, task3] >> task4
