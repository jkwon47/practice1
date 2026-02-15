"""Amazon careers scraper."""
from datetime import datetime
from typing import List, Optional
import hashlib
import re

from .base import BaseScraper
from database.models import Job


class AmazonScraper(BaseScraper):
    """Scraper for Amazon careers page."""

    def __init__(self, careers_url: str):
        """Initialize Amazon scraper."""
        super().__init__("Amazon", careers_url)

    def scrape(self) -> List[Job]:
        """
        Scrape jobs from Amazon careers page.

        Note: Amazon's job search may use APIs. This is a template implementation.

        Returns:
            List[Job]: List of scraped jobs
        """
        jobs = []

        # Amazon may have a public API for job searches
        # Check their careers page for API endpoints or use browser automation

        html = self.fetch_page(self.careers_url)
        if not html:
            return jobs

        soup = self.parse_html(html)

        # Template parsing - needs customization based on actual structure
        job_results = soup.find_all('div', class_='job-tile')  # Placeholder

        for result in job_results:
            try:
                job = self._parse_job_result(result)
                if job:
                    jobs.append(job)
            except Exception as e:
                self.logger.error(f"Error parsing job result: {e}")
                continue

        return jobs

    def _parse_job_result(self, result) -> Optional[Job]:
        """
        Parse individual job result.

        Args:
            result: BeautifulSoup element containing job result

        Returns:
            Optional[Job]: Parsed job or None
        """
        try:
            # Extract title
            title_link = result.find('a', class_='job-title-link')
            if not title_link:
                return None

            title = title_link.get_text(strip=True)
            url = title_link.get('href', '')

            # Generate job ID
            job_id = hashlib.md5(f"amazon_{url}".encode()).hexdigest()

            # Extract location
            location_elem = result.find('span', class_='location-name')
            location = location_elem.get_text(strip=True) if location_elem else "Unknown"

            # Parse salary if available
            salary_elem = result.find('div', class_='salary-info')
            salary_max = None
            if salary_elem:
                salary_text = salary_elem.get_text(strip=True)
                # Try to extract max salary from text like "$150,000 - $250,000"
                salary_max = self._extract_max_salary(salary_text)

            # Parse posted date
            date_elem = result.find('span', class_='posted-date')
            posted_date = self._parse_posted_date(date_elem.get_text(strip=True)) if date_elem else datetime.now()

            # Get description
            desc_elem = result.find('div', class_='job-description')
            description = desc_elem.get_text(strip=True) if desc_elem else None

            return Job(
                job_id=job_id,
                company=self.company_name,
                title=title,
                location=location,
                salary_min=None,
                salary_max=salary_max,
                posted_date=posted_date,
                url=url if url.startswith('http') else f"https://www.amazon.jobs{url}",
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
            # Look for patterns like "$200,000" or "$200K"
            amounts = re.findall(r'\$\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*[Kk]?', salary_text)
            if amounts:
                # Convert to float, handling K suffix
                max_amount = max([float(amt.replace(',', '')) for amt in amounts])
                if 'k' in salary_text.lower() and max_amount < 1000:
                    max_amount *= 1000
                return max_amount
        except Exception:
            pass
        return None

    def _parse_posted_date(self, date_text: str) -> datetime:
        """
        Parse posted date from text.

        Args:
            date_text: Text containing date

        Returns:
            datetime: Parsed date or current date
        """
        # Simple implementation - would need more sophisticated parsing
        # for different date formats
        try:
            if 'today' in date_text.lower():
                return datetime.now()
            # Add more date parsing logic as needed
            return datetime.now()
        except Exception:
            return datetime.now()
