"""Database models for job scraper."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Job:
    """Represents a job posting."""

    job_id: str
    company: str
    title: str
    location: str
    salary_min: Optional[float]
    salary_max: Optional[float]
    posted_date: datetime
    url: str
    description: Optional[str] = None
    scraped_at: Optional[datetime] = None

    def __post_init__(self):
        """Set scraped_at to current time if not provided."""
        if self.scraped_at is None:
            self.scraped_at = datetime.now()

    def meets_criteria(self, min_salary: float, days_back: int, target_keywords: list, excluded_keywords: list) -> bool:
        """
        Check if job meets filtering criteria.

        Args:
            min_salary: Minimum salary max threshold
            days_back: Maximum days since posting
            target_keywords: Keywords that should be in title/description
            excluded_keywords: Keywords that disqualify the job

        Returns:
            bool: True if job meets all criteria
        """
        # Check salary requirement
        if self.salary_max is None or self.salary_max <= min_salary:
            return False

        # Check posting date
        days_old = (datetime.now() - self.posted_date).days
        if days_old > days_back:
            return False

        # Check for excluded keywords in title
        title_lower = self.title.lower()
        for keyword in excluded_keywords:
            if keyword.lower() in title_lower:
                return False

        # Check for target keywords in title or description
        search_text = title_lower
        if self.description:
            search_text += " " + self.description.lower()

        has_target_keyword = any(keyword.lower() in search_text for keyword in target_keywords)
        if not has_target_keyword:
            return False

        return True
