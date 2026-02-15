"""Filtering utilities for job postings."""
from datetime import datetime, timedelta
from typing import List
from database.models import Job


class JobFilter:
    """Filter jobs based on various criteria."""

    @staticmethod
    def filter_jobs(
        jobs: List[Job],
        min_salary: float,
        days_back: int,
        target_keywords: List[str],
        excluded_keywords: List[str]
    ) -> List[Job]:
        """
        Filter jobs based on criteria.

        Args:
            jobs: List of Job objects to filter
            min_salary: Minimum salary max threshold
            days_back: Maximum days since posting
            target_keywords: Keywords that should be in title/description
            excluded_keywords: Keywords that disqualify the job

        Returns:
            List[Job]: Filtered list of jobs
        """
        filtered_jobs = []
        for job in jobs:
            if job.meets_criteria(min_salary, days_back, target_keywords, excluded_keywords):
                filtered_jobs.append(job)
        return filtered_jobs

    @staticmethod
    def has_target_keywords(text: str, keywords: List[str]) -> bool:
        """
        Check if text contains any of the target keywords.

        Args:
            text: Text to search
            keywords: List of keywords to look for

        Returns:
            bool: True if any keyword is found
        """
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)

    @staticmethod
    def has_excluded_keywords(text: str, keywords: List[str]) -> bool:
        """
        Check if text contains any excluded keywords.

        Args:
            text: Text to search
            keywords: List of excluded keywords

        Returns:
            bool: True if any excluded keyword is found
        """
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)

    @staticmethod
    def is_recent(posted_date: datetime, days_back: int) -> bool:
        """
        Check if job was posted within the specified timeframe.

        Args:
            posted_date: Job posting date
            days_back: Maximum days since posting

        Returns:
            bool: True if job is recent enough
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        return posted_date >= cutoff_date
