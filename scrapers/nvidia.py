"""NVIDIA careers scraper."""
from datetime import datetime
from typing import List, Optional
import hashlib
import re

from .base import BaseScraper
from database.models import Job


class NVIDIAScraper(BaseScraper):
    """Scraper for NVIDIA careers page."""

    def __init__(self, careers_url: str):
        """Initialize NVIDIA scraper."""
        super().__init__("NVIDIA", careers_url)

    def scrape(self) -> List[Job]:
        """
        Scrape jobs from NVIDIA careers page.

        Note: NVIDIA uses Workday for their careers portal, which typically
        requires API access or browser automation. This is a template.

        Returns:
            List[Job]: List of scraped jobs
        """
        jobs = []

        # Workday sites often use APIs - look for API endpoints
        # or use Selenium for JavaScript rendering

        html = self.fetch_page(self.careers_url)
        if not html:
            return jobs

        soup = self.parse_html(html)

        # Template parsing for Workday-style pages
        job_listings = soup.find_all('li', class_='WGKV')  # Workday common class

        for listing in job_listings:
            try:
                job = self._parse_job_listing(listing)
                if job:
                    jobs.append(job)
            except Exception as e:
                self.logger.error(f"Error parsing job listing: {e}")
                continue

        return jobs

    def _parse_job_listing(self, listing) -> Optional[Job]:
        """
        Parse individual job listing.

        Args:
            listing: BeautifulSoup element containing job listing

        Returns:
            Optional[Job]: Parsed job or None
        """
        try:
            # Workday typically structures data differently
            # This is a simplified template

            title_elem = listing.find('a', {'data-automation-id': 'jobTitle'})
            if not title_elem:
                title_elem = listing.find('h3')

            if not title_elem:
                return None

            title = title_elem.get_text(strip=True)
            url = title_elem.get('href', '')

            # Generate job ID
            job_id = hashlib.md5(f"nvidia_{url}".encode()).hexdigest()

            # Extract location
            location_elem = listing.find('dd', {'data-automation-id': 'location'})
            if not location_elem:
                location_elem = listing.find('span', class_='location')
            location = location_elem.get_text(strip=True) if location_elem else "Unknown"

            # NVIDIA typically doesn't list salaries publicly on job postings
            salary_max = None

            # Parse posted date
            date_elem = listing.find('dd', {'data-automation-id': 'postedOn'})
            posted_date = datetime.now()  # Would need actual date parsing

            # Get description preview
            desc_elem = listing.find('dd', {'data-automation-id': 'jobDescription'})
            description = desc_elem.get_text(strip=True) if desc_elem else None

            return Job(
                job_id=job_id,
                company=self.company_name,
                title=title,
                location=location,
                salary_min=None,
                salary_max=salary_max,
                posted_date=posted_date,
                url=url if url.startswith('http') else f"https://nvidia.wd5.myworkdayjobs.com{url}",
                description=description
            )
        except Exception as e:
            self.logger.error(f"Error parsing job: {e}")
            return None
