import re

import requests
from bs4 import BeautifulSoup

from src.database.database import Job
from src.database.database_management import DBManagement
from src.web_srapping.scrap_base import Scrap


class CVBankas(Scrap):
    def __init__(self, jobs: list = None):
        if jobs:
            self.jobs = '+'.join(jobs)
        else:
            self.jobs = 'data+engineering'
        self.db = DBManagement()

    def _extract_page(self) -> BeautifulSoup:
        """
        Extracts data from DB.
        :return: BeautifulSoup object
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/117.0.0.0 Safari/537.36'}
        url = f'https://www.cvbankas.lt/?keyw={self.jobs}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def _transport_data(self, soup: BeautifulSoup) -> None:
        """
        Ads values to DB
        :param soup: BeautifulSoup
        :return: None
        """
        jobs = soup.findAll('a', class_='list_a can_visited list_a_has_logo')
        for job in jobs:
            url = job.get('href', None)
            if self.db.check_if_job_exists_in_db(url):
                continue
            title = job.find('h3', class_='list_h3').text[:80].lower()
            company = job.find('span', class_='dib mt5 mr10').text
            region = job.find('span', class_=f'list_city').text
            try:
                salary = job.find('span', class_=f'salary_amount').text
                salary = int(re.findall(r'\d+', salary)[0])
            except AttributeError:
                salary = 0
            job_ = Job(portal='CVBankas', company=company, job_title=title, link_to_job=url, region=region,
                       salary=salary)
            self.db.add_value_to_db(job_)

    def run_scrap(self) -> None:
        """
        Runs page scrap
        """
        soup = self._extract_page()
        self._transport_data(soup)
        self.db.close_session()
