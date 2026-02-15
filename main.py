#!/usr/bin/env python3
"""
Job Scraper - Main Entry Point

Monitors job postings from major tech companies for venture capital
and corporate development positions with high salary ranges.
"""
import logging
import sys
from typing import List

from config import (
    COMPANIES,
    TARGET_KEYWORDS,
    EXCLUDED_KEYWORDS,
    MIN_SALARY,
    DAYS_BACK
)
from database import DatabaseManager
from database.models import Job
from utils import JobFilter
from scrapers import (
    GoogleScraper,
    MetaScraper,
    AmazonScraper,
    MicrosoftScraper,
    NVIDIAScraper,
    AMDScraper
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('job_scraper.log')
    ]
)
logger = logging.getLogger(__name__)


class JobScraperOrchestrator:
    """Orchestrates job scraping across multiple companies."""

    def __init__(self):
        """Initialize the orchestrator."""
        self.db_manager = DatabaseManager()
        self.job_filter = JobFilter()
        self.scrapers = self._initialize_scrapers()

    def _initialize_scrapers(self) -> dict:
        """
        Initialize all company scrapers.

        Returns:
            dict: Dictionary mapping company names to scraper instances
        """
        scrapers = {}

        for company_key, company_config in COMPANIES.items():
            if not company_config.get('enabled', True):
                continue

            scraper_class = self._get_scraper_class(company_key)
            if scraper_class:
                scrapers[company_key] = scraper_class(company_config['careers_url'])
            else:
                logger.warning(f"No scraper class found for {company_key}")

        return scrapers

    def _get_scraper_class(self, company_key: str):
        """
        Get the appropriate scraper class for a company.

        Args:
            company_key: Company identifier

        Returns:
            Scraper class or None
        """
        scraper_map = {
            'google': GoogleScraper,
            'meta': MetaScraper,
            'amazon': AmazonScraper,
            'microsoft': MicrosoftScraper,
            'nvidia': NVIDIAScraper,
            'amd': AMDScraper
        }
        return scraper_map.get(company_key)

    def scrape_all_companies(self) -> List[Job]:
        """
        Scrape jobs from all enabled companies.

        Returns:
            List[Job]: All scraped jobs (unfiltered)
        """
        all_jobs = []

        for company_key, scraper in self.scrapers.items():
            logger.info(f"Scraping {COMPANIES[company_key]['name']}...")
            try:
                jobs = scraper.run()
                all_jobs.extend(jobs)
                logger.info(f"Found {len(jobs)} jobs from {COMPANIES[company_key]['name']}")
            except Exception as e:
                logger.error(f"Error scraping {company_key}: {e}")
                continue

        return all_jobs

    def filter_jobs(self, jobs: List[Job]) -> List[Job]:
        """
        Filter jobs based on criteria.

        Args:
            jobs: List of jobs to filter

        Returns:
            List[Job]: Filtered jobs meeting all criteria
        """
        filtered = self.job_filter.filter_jobs(
            jobs=jobs,
            min_salary=MIN_SALARY,
            days_back=DAYS_BACK,
            target_keywords=TARGET_KEYWORDS,
            excluded_keywords=EXCLUDED_KEYWORDS
        )
        return filtered

    def save_jobs(self, jobs: List[Job]) -> int:
        """
        Save jobs to database.

        Args:
            jobs: List of jobs to save

        Returns:
            int: Number of new jobs added
        """
        return self.db_manager.add_jobs_batch(jobs)

    def print_summary(self, total_scraped: int, total_filtered: int, new_jobs_added: int):
        """
        Print summary of scraping session.

        Args:
            total_scraped: Total jobs scraped
            total_filtered: Total jobs after filtering
            new_jobs_added: Number of new jobs added to database
        """
        logger.info("=" * 60)
        logger.info("SCRAPING SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total jobs scraped: {total_scraped}")
        logger.info(f"Jobs matching criteria: {total_filtered}")
        logger.info(f"New jobs added to database: {new_jobs_added}")
        logger.info(f"Duplicate jobs skipped: {total_filtered - new_jobs_added}")

        # Get and print database stats
        stats = self.db_manager.get_stats()
        logger.info("=" * 60)
        logger.info("DATABASE STATISTICS")
        logger.info("=" * 60)
        logger.info(f"Total jobs in database: {stats['total_jobs']}")
        logger.info("Jobs by company:")
        for company, count in stats['jobs_by_company'].items():
            logger.info(f"  {company}: {count}")
        if stats['average_salary_max']:
            logger.info(f"Average max salary: ${stats['average_salary_max']:,.0f}")
        logger.info("=" * 60)

    def run(self):
        """Run the complete scraping workflow."""
        logger.info("Starting job scraper...")
        logger.info(f"Target keywords: {', '.join(TARGET_KEYWORDS)}")
        logger.info(f"Excluded keywords: {', '.join(EXCLUDED_KEYWORDS)}")
        logger.info(f"Minimum salary max: ${MIN_SALARY:,}")
        logger.info(f"Days back: {DAYS_BACK}")
        logger.info("=" * 60)

        # Scrape all companies
        all_jobs = self.scrape_all_companies()
        logger.info(f"Scraped {len(all_jobs)} total jobs")

        # Filter jobs
        filtered_jobs = self.filter_jobs(all_jobs)
        logger.info(f"Filtered down to {len(filtered_jobs)} jobs meeting criteria")

        # Save to database
        new_jobs_added = self.save_jobs(filtered_jobs)

        # Print summary
        self.print_summary(
            total_scraped=len(all_jobs),
            total_filtered=len(filtered_jobs),
            new_jobs_added=new_jobs_added
        )

        logger.info("Job scraping completed successfully!")


def main():
    """Main entry point."""
    try:
        orchestrator = JobScraperOrchestrator()
        orchestrator.run()
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
