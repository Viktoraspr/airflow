import re

import requests
from bs4 import BeautifulSoup

from src.database.database import Job
from src.database.database_management import DBManagement
from src.web_srapping.scrap_base import Scrap


class CvOnline(Scrap):
    def __init__(self, jobs: list = None):
        if jobs:
            self.jobs = '%20'.join(jobs)
        else:
            self.jobs = 'data%20engineer'
        self.db = DBManagement()

    def _extract_page(self):
        """
        Extracts data from DB.
        :return: BeautifulSoup object
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/117.0.0.0 Safari/537.36'}
        url = f'https://www.cvonline.lt/lt/search?limit=20&offset=0' \
              f'&categories%5B0%5D=INFORMATION_TECHNOLOGY&keywords%5B0%5D={self.jobs}' \
              f'&towns%5B0%5D=540&fuzzy=true&suitableForRefugees=false&isHourlySalary=false&isRemoteWork=false' \
              f'&isQuickApply=false'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def _transport_data(self, soup):
        """
        Ads values to DB
        :param soup: BeautifulSoup
        :return: None
        """
        jobs = soup.findAll('li', class_='jsx-1871295890 jsx-78775730 vacancies-list__item false')
        id_locator = '3024910437'
        for job in jobs:
            url = job.find('a', class_=f'jsx-{id_locator}').get('href', None)
            if self.db.check_if_job_exists_in_db(url):
                continue
            title = job.find('span', class_=f'jsx-{id_locator} vacancy-item__title').text[:80].lower()
            company = job.find('div', class_=f'jsx-{id_locator} vacancy-item__column').text
            region = job.find('div', class_=f'jsx-{id_locator} vacancy-item__column vacancy-item__locations').text
            try:
                salary = job.find('span', class_=f'jsx-{id_locator} vacancy-item__salary-label').text
                salary = int(re.findall(r'\d+', salary)[0])
            except AttributeError:
                salary = 0
            job_ = Job(portal='CVOnline', company=company, job_title=title, link_to_job=url, region=region,
                       salary=salary)
            self.db.add_value_to_db(job_)

    def run_scrap(self):
        """
        Runs page scrap
        """
        soup = self._extract_page()
        self._transport_data(soup)
        self.db.close_session()
