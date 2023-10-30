"""
This file is using for creating tables in DB and
"""

from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from src.constants.credentials import URL

Base: Any = declarative_base()
engine = create_engine(URL)


class Job(Base):
    """
    Class describe table 'cities' in database
    """
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    portal = Column(String(50))
    company = Column(String(80))
    job_title = Column(String(80))
    link_to_job = Column(String(200))
    job_type = Column(String(120), default='')
    region = Column(String(100))
    salary = Column(Integer)
    timestamp = Column(DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f'Job (id={self.id!r}, name={self.job_title!r}, portal={self.portal})'


class DataAboutDataEngineer(Base):
    """
    Class describe table 'jobs_info' in database
    """
    __tablename__ = "jobs_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    jobs_number_today = Column(Integer)
    remote_jobs_today = Column(Integer)
    maximum_per_day = Column(Integer)
    minimum_per_day = Column(Integer)
    average_per_day = Column(Integer)
    standard_deviation_per_day = Column(Integer)
    maximum_per_total = Column(Integer)
    minimum_per_total = Column(Integer)
    average_per_total = Column(Integer)
    standard_deviation_per_total = Column(Integer)

    def __repr__(self) -> str:
        return f'Job (id={self.id!r}, name={self.date!r})'


Base.metadata.create_all(engine)
