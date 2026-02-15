"""AMD careers scraper."""
from datetime import datetime
from typing import List, Optional
import hashlib
import re

from .base import BaseScraper
from database.models import Job


class AMDScraper(BaseScraper):
    """Scraper for AMD careers page."""

    def __init__(self, careers_url: str):
        """Initialize AMD scraper."""
        super().__init__("AMD", careers_url)

    def scrape(self) -> List[Job]:
        """
        Scrape jobs from AMD careers page.

        Note: AMD's careers portal structure may vary. This is a template.

        Returns:
            List[Job]: List of scraped jobs
        """
        jobs = []

        html = self.fetch_page(self.careers_url)
        if not html:
            return jobs

        soup = self.parse_html(html)

        # Template parsing - customize based on actual structure
        job_cards = soup.find_all('div', class_='job-card')  # Placeholder

        for card in job_cards:
            try:
                job = self._parse_job_card(card)
                if job:
                    jobs.append(job)
            except Exception as e:
                self.logger.error(f"Error parsing job card: {e}")
                continue

        return jobs

    def _parse_job_card(self, card) -> Optional[Job]:
        """
        Parse individual job card.

        Args:
            card: BeautifulSoup element containing job card

        Returns:
            Optional[Job]: Parsed job or None
        """
        try:
            # Extract title
            title_elem = card.find('h3', class_='job-title')
            if not title_elem:
                title_elem = card.find('a', class_='job-link')

            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)

            # Get URL
            link_elem = card.find('a', class_='job-link')
            if not link_elem:
                link_elem = title_elem if title_elem.name == 'a' else None

            url = link_elem.get('href', '') if link_elem else ''

            # Generate job ID
            job_id = hashlib.md5(f"amd_{url}_{title}".encode()).hexdigest()

            # Extract location
            location_elem = card.find('span', class_='job-location')
            location = location_elem.get_text(strip=True) if location_elem else "Unknown"

            # Parse salary if available (often not listed)
            salary_elem = card.find('div', class_='compensation')
            salary_max = None
            if salary_elem:
                salary_text = salary_elem.get_text(strip=True)
                salary_max = self._extract_max_salary(salary_text)

            # Parse posted date
            date_elem = card.find('time')
            if date_elem and date_elem.get('datetime'):
                try:
                    posted_date = datetime.fromisoformat(date_elem.get('datetime').replace('Z', '+00:00'))
                except Exception:
                    posted_date = datetime.now()
            else:
                posted_date = datetime.now()

            # Get description
            desc_elem = card.find('div', class_='job-description')
            description = desc_elem.get_text(strip=True) if desc_elem else None

            return Job(
                job_id=job_id,
                company=self.company_name,
                title=title,
                location=location,
                salary_min=None,
                salary_max=salary_max,
                posted_date=posted_date,
                url=url if url.startswith('http') else f"https://jobs.amd.com{url}",
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
            # Look for salary patterns
            amounts = re.findall(r'\$\s*(\d{1,3}(?:,\d{3})*)\s*[Kk]?', salary_text)
            if amounts:
                max_amount = max([float(amt.replace(',', '')) for amt in amounts])
                if 'k' in salary_text.lower() and max_amount < 1000:
                    max_amount *= 1000
                return max_amount
        except Exception:
            pass
        return None
