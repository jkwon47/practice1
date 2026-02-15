"""Base scraper class for all company-specific scrapers."""
import time
import logging
from abc import ABC, abstractmethod
from typing import List, Optional
import requests
from bs4 import BeautifulSoup

from database.models import Job
from config import REQUEST_TIMEOUT, USER_AGENT, REQUEST_DELAY


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class BaseScraper(ABC):
    """Abstract base class for company-specific job scrapers."""

    def __init__(self, company_name: str, careers_url: str):
        """
        Initialize base scraper.

        Args:
            company_name: Name of the company
            careers_url: URL of the company's careers page
        """
        self.company_name = company_name
        self.careers_url = careers_url
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})

    def fetch_page(self, url: str, params: Optional[dict] = None) -> Optional[str]:
        """
        Fetch a web page with error handling.

        Args:
            url: URL to fetch
            params: Optional query parameters

        Returns:
            Optional[str]: HTML content or None if fetch failed
        """
        try:
            self.logger.info(f"Fetching {url}")
            response = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            time.sleep(REQUEST_DELAY)  # Be respectful with rate limiting
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content with BeautifulSoup.

        Args:
            html: HTML content to parse

        Returns:
            BeautifulSoup: Parsed HTML
        """
        return BeautifulSoup(html, 'html.parser')

    @abstractmethod
    def scrape(self) -> List[Job]:
        """
        Scrape jobs from the company's careers page.
        Must be implemented by each company-specific scraper.

        Returns:
            List[Job]: List of scraped jobs
        """
        pass

    def run(self) -> List[Job]:
        """
        Run the scraper and return jobs.

        Returns:
            List[Job]: List of scraped jobs
        """
        self.logger.info(f"Starting scrape for {self.company_name}")
        try:
            jobs = self.scrape()
            self.logger.info(f"Found {len(jobs)} jobs for {self.company_name}")
            return jobs
        except Exception as e:
            self.logger.error(f"Error scraping {self.company_name}: {e}")
            return []
