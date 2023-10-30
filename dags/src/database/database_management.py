"""
This file contains class DBManagement - it's used for connection with DB using CRUD operations
"""

from datetime import datetime, date
from typing import Any, List, Tuple

from sqlalchemy import create_engine, Date, cast
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import text

from src.constants.credentials import URL
from src.database.database import Job, DataAboutDataEngineer


class DBManagement:
    """
    This class is for CRUD operations.
    """
    def __init__(self, url: str = URL):
        self.url: str = url
        self.engine = create_engine(self.url)
        base: Any = declarative_base()
        base.metadata.create_all(bind=self.engine)
        self.session_ = sessionmaker(bind=self.engine)
        self.session = self.session_()

    def add_value_to_db(self, value):
        """
        Method injects data in DB
        :param value: Object from sqlalchemy table
        :return: None
        """
        self.session.add(value)
        self.session.commit()

    def add_values_to_db(self, data: list) -> None:
        """
        Method injects data in DB
        :param data: list of data, needed to be injected in DB
        :return: None
        """
        self.session.add_all(data)
        self.session.commit()

    def check_if_job_exists_in_db(self, link_to_job: str) -> bool:
        """
        Needs to check if job is already exists in db
        :param link_to_job: value, which should be in DB
        :return: None
        """
        return self.session.query(Job).filter_by(link_to_job=link_to_job).one_or_none()

    def get_values_from_job_table(self) -> List:
        """
        Returns values from Job table.
        :return: all jobs,which exits in  DB
        """
        return self.session.query(Job).all()

    def delete_values_from_db(self) -> None:
        """
        Deletes all raw in job table.
        :return: None
        """
        self.session.query(Job).delete()
        self.session.commit()

    def close_session(self) -> None:
        """
        Close session
        :return: None
        """
        self.session.close()

    def execute_query(self, sql_query: str) -> List:
        """
        Executes any sql query
        :param sql_query: sql query
        :return: Values from DB
        """
        result = self.session.execute(text(sql_query))
        return result.fetchall()

    def get_remote_jobs(self, sql_query: str, values: list = None) -> int:
        """
        Gets all jobs from the list
        :param sql_query:
        :param values: any jobs to search in DB
        :return: number of searched jobs
        """
        if not values:
            values = ['remote', 'nuotolin']

        result = 0
        for value in values:
            remote_jobs_query = f"{sql_query[:-1]} and job_type like '%{value}%';"
            result += self.execute_query(remote_jobs_query)[0][0]
        return result

    def get_data_salary(self) -> Tuple[List, ...]:
        """
        Gets all data related salary -
        :return: List of values
        """
        today = datetime.today()
        sql_query_total = """
        select min(salary), max(salary), avg(salary), stddev(salary)
        from jobs
        where salary > 0 and job_title like '%data engin%';
        """
        result_total = self.execute_query(sql_query_total)[0]
        result_total = [int(round(r, 0)) for r in result_total]

        sql_query_total = f"""
        select min(salary), max(salary), avg(salary), stddev(salary)
        from jobs
        where timestamp BETWEEN '{today.year}/{today.month}/{today.day}' and
        '{today.year}/{today.month}/{today.day+1}' and salary > 0 and job_title like '%data engin%';
        """
        result_today = self.execute_query(sql_query_total)[0]
        print(result_today)
        try:
            result_today = [int(round(r, 0)) for r in result_today]
        except TypeError:
            result_today = [0, 0, 0, 0]
        return result_total, result_today

    def delete_today_data(self):
        """
        Deletes today values from jobs_info table
        :return: None
        """
        try:
            value = self.session.query(DataAboutDataEngineer).filter(cast(DataAboutDataEngineer.date,
                                                                          Date) == date.today()).one()
            self.session.delete(value)
            self.session.commit()
        except NoResultFound:
            pass

    def add_data_to_jobs_data_table(self):
        """
        Adds data jobs_info table.
        :return: None
        """
        today = datetime.today()

        jobs_number_today_sql = f"""
        select count(id)
        from jobs
        where timestamp BETWEEN '{today.year}/{today.month}/{today.day}' and
        '{today.year}/{today.month}/{today.day+1}' and job_title like '%data engineer%';"""
        jobs_number_today = self.execute_query(jobs_number_today_sql)[0][0]

        remote_jobs = self.get_remote_jobs(jobs_number_today_sql)
        salary = self.get_data_salary()

        self.delete_today_data()

        data = DataAboutDataEngineer(
            date=datetime.today(),
            jobs_number_today=jobs_number_today,
            remote_jobs_today=remote_jobs,
            maximum_per_day=salary[1][1],
            minimum_per_day=salary[1][0],
            average_per_day=salary[1][2],
            standard_deviation_per_day=salary[1][3],
            maximum_per_total=salary[0][1],
            minimum_per_total=salary[0][0],
            average_per_total=salary[0][2],
            standard_deviation_per_total=salary[0][3],

        )

        self.session.add(data)
        self.session.commit()
