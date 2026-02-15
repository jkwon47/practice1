"""Microsoft careers scraper."""
from datetime import datetime
from typing import List, Optional
import hashlib
import re

from .base import BaseScraper
from database.models import Job


class MicrosoftScraper(BaseScraper):
    """Scraper for Microsoft careers page."""

    def __init__(self, careers_url: str):
        """Initialize Microsoft scraper."""
        super().__init__("Microsoft", careers_url)

    def scrape(self) -> List[Job]:
        """
        Scrape jobs from Microsoft careers page.

        Note: Microsoft careers may use dynamic content loading.
        This is a template implementation.

        Returns:
            List[Job]: List of scraped jobs
        """
        jobs = []

        html = self.fetch_page(self.careers_url)
        if not html:
            return jobs

        soup = self.parse_html(html)

        # Template parsing - customize based on actual page structure
        job_items = soup.find_all('li', class_='jobs-list-item')  # Placeholder

        for item in job_items:
            try:
                job = self._parse_job_item(item)
                if job:
                    jobs.append(job)
            except Exception as e:
                self.logger.error(f"Error parsing job item: {e}")
                continue

        return jobs

    def _parse_job_item(self, item) -> Optional[Job]:
        """
        Parse individual job item.

        Args:
            item: BeautifulSoup element containing job item

        Returns:
            Optional[Job]: Parsed job or None
        """
        try:
            # Extract title and URL
            title_elem = item.find('h2', class_='job-title')
            if not title_elem:
                return None

            title_link = title_elem.find('a')
            if not title_link:
                return None

            title = title_link.get_text(strip=True)
            url = title_link.get('href', '')

            # Generate job ID
            job_id = hashlib.md5(f"microsoft_{url}".encode()).hexdigest()

            # Extract location
            location_elem = item.find('span', class_='job-location')
            location = location_elem.get_text(strip=True) if location_elem else "Unknown"

            # Parse salary if available
            # Microsoft often includes salary ranges for certain positions
            salary_elem = item.find('span', class_='salary-range')
            salary_max = None
            if salary_elem:
                salary_text = salary_elem.get_text(strip=True)
                salary_max = self._extract_max_salary(salary_text)

            # Parse posted date
            date_elem = item.find('time')
            if date_elem and date_elem.get('datetime'):
                try:
                    posted_date = datetime.fromisoformat(date_elem.get('datetime').replace('Z', '+00:00'))
                except Exception:
                    posted_date = datetime.now()
            else:
                posted_date = datetime.now()

            # Get description
            desc_elem = item.find('div', class_='job-description')
            description = desc_elem.get_text(strip=True) if desc_elem else None

            return Job(
                job_id=job_id,
                company=self.company_name,
                title=title,
                location=location,
                salary_min=None,
                salary_max=salary_max,
                posted_date=posted_date,
                url=url if url.startswith('http') else f"https://careers.microsoft.com{url}",
                description=description
            )
        except Exception as e:
            self.logger.error(f"Error parsing job: {e}")
            return None

    def _extract_max_salary(self, salary_text: str) -> Optional[float]:
        """
        Extract maximum salary from salary text.

        Args:
            salary_text: Text containing salary information

        Returns:
            Optional[float]: Maximum salary or None
        """
        try:
            # Look for patterns like "$150,000 - $250,000" or "$200K - $300K"
            amounts = re.findall(r'\$\s*(\d{1,3}(?:,\d{3})*)\s*[Kk]?', salary_text)
            if amounts:
                max_amount = max([float(amt.replace(',', '')) for amt in amounts])
                if 'k' in salary_text.lower() and max_amount < 1000:
                    max_amount *= 1000
                return max_amount
        except Exception:
            pass
        return None
