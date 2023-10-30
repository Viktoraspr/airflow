from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


class Scrap(ABC):
    """
    Abstract class for web scrapping
    """

    @abstractmethod
    def _extract_page(self):
        """
        Extracts data from web page
        """
        pass

    @abstractmethod
    def _transport_data(self, soup: BeautifulSoup):
        """
        Injects data in DB
        """
        pass

    @abstractmethod
    def run_scrap(self):
        """Runs scrap"""
        pass
