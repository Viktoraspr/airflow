import re

import requests
from bs4 import BeautifulSoup

from src.database.database import Job
from src.database.database_management import DBManagement
from src.web_srapping.scrap_base import Scrap


class CvMarket(Scrap):
    def __init__(self, jobs: list = None):
        if jobs:
            self.jobs = '+'.join(jobs)
        else:
            self.jobs = 'data+engineer'
        self.db = DBManagement()

    def _extract_page(self):
        """
        Extracts data from DB.
        :return: BeautifulSoup object
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/117.0.0.0 Safari/537.36'}
        url = f'https://www.cvmarket.lt/darbo-skelbimai?op=search&search%5Bjob_salary%5D=3&ga_track=homepage&search' \
              f'%5Bkeyword%5D={self.jobs}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def _transport_data(self, soup):
        """
        Ads values to DB
        :param soup: BeautifulSoup
        :return: None
        """
        jobs = soup.findAll('article', class_='flex-col lg:flex-row py-6 px-5 lg:px-6 xl:px-7.5 bg-white lg:rounded-xl '
                                              'shadow hover:shadow-md cursor-pointer relative flex h-full')
        for job in jobs:
            url = job.find('a', class_='break-words visited:text-gray-300 jobad-url').get('href', None)
            if self.db.check_if_job_exists_in_db(url):
                continue
            title = job.find('h2', class_='xl:text-xl font-bold mt-2 hover:underline').text[:80].lower()
            company = job.find('span', class_='job-company mr-5').text

            region = job.find('span',
                              class_='bg-blue-50 text-slate-500 py-1.5 px-3 font-bold text-sm rounded-full flex w-fit '
                                     'h-fit justify-center items-center space-x-1.5 '
                                     'cursor-defaults leading-4 location').text
            try:
                salary = job.find('span', class_='font-bold text-blue-500 visited-group:text-gray-300 mr-2').text
                salary = int(re.findall(r'\d+', salary)[0])
            except AttributeError:
                salary = 0
            job_type = job.find('span', class_='flex items-start space-x-1 md:items-center').text.strip()
            job_ = Job(portal='CVMarket', company=company, job_title=title, link_to_job=url, region=region.strip(),
                       salary=salary, job_type=job_type)
            self.db.add_value_to_db(job_)

    def run_scrap(self):
        """
        Runs page scrap
        """
        soup = self._extract_page()
        self._transport_data(soup)
        self.db.close_session()
