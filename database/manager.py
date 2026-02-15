"""Database manager for SQLite operations."""
import sqlite3
from datetime import datetime
from typing import List, Optional
from contextlib import contextmanager

from .models import Job
from config import DATABASE_PATH


class DatabaseManager:
    """Manages SQLite database operations for job postings."""

    def __init__(self, db_path: str = DATABASE_PATH):
        """
        Initialize database manager.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def init_database(self):
        """Create database tables if they don't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    company TEXT NOT NULL,
                    title TEXT NOT NULL,
                    location TEXT NOT NULL,
                    salary_min REAL,
                    salary_max REAL,
                    posted_date TEXT NOT NULL,
                    url TEXT NOT NULL,
                    description TEXT,
                    scraped_at TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create indices for better query performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_company ON jobs(company)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_posted_date ON jobs(posted_date)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_salary_max ON jobs(salary_max)
            """)

    def job_exists(self, job_id: str) -> bool:
        """
        Check if a job already exists in the database.

        Args:
            job_id: Unique job identifier

        Returns:
            bool: True if job exists
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM jobs WHERE job_id = ?", (job_id,))
            return cursor.fetchone() is not None

    def add_job(self, job: Job) -> bool:
        """
        Add a job to the database if it doesn't already exist.

        Args:
            job: Job object to add

        Returns:
            bool: True if job was added, False if it already existed
        """
        if self.job_exists(job.job_id):
            return False

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO jobs (
                    job_id, company, title, location,
                    salary_min, salary_max, posted_date, url,
                    description, scraped_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job.job_id,
                job.company,
                job.title,
                job.location,
                job.salary_min,
                job.salary_max,
                job.posted_date.isoformat(),
                job.url,
                job.description,
                job.scraped_at.isoformat()
            ))
            return True

    def add_jobs_batch(self, jobs: List[Job]) -> int:
        """
        Add multiple jobs to the database.

        Args:
            jobs: List of Job objects to add

        Returns:
            int: Number of new jobs added
        """
        added_count = 0
        for job in jobs:
            if self.add_job(job):
                added_count += 1
        return added_count

    def get_all_jobs(self) -> List[Job]:
        """
        Retrieve all jobs from the database.

        Returns:
            List[Job]: List of all jobs
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jobs ORDER BY posted_date DESC")
            rows = cursor.fetchall()

            jobs = []
            for row in rows:
                job = Job(
                    job_id=row['job_id'],
                    company=row['company'],
                    title=row['title'],
                    location=row['location'],
                    salary_min=row['salary_min'],
                    salary_max=row['salary_max'],
                    posted_date=datetime.fromisoformat(row['posted_date']),
                    url=row['url'],
                    description=row['description'],
                    scraped_at=datetime.fromisoformat(row['scraped_at'])
                )
                jobs.append(job)

            return jobs

    def get_jobs_by_company(self, company: str) -> List[Job]:
        """
        Retrieve jobs for a specific company.

        Args:
            company: Company name

        Returns:
            List[Job]: List of jobs for the company
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM jobs WHERE company = ? ORDER BY posted_date DESC",
                (company,)
            )
            rows = cursor.fetchall()

            jobs = []
            for row in rows:
                job = Job(
                    job_id=row['job_id'],
                    company=row['company'],
                    title=row['title'],
                    location=row['location'],
                    salary_min=row['salary_min'],
                    salary_max=row['salary_max'],
                    posted_date=datetime.fromisoformat(row['posted_date']),
                    url=row['url'],
                    description=row['description'],
                    scraped_at=datetime.fromisoformat(row['scraped_at'])
                )
                jobs.append(job)

            return jobs

    def get_stats(self) -> dict:
        """
        Get statistics about stored jobs.

        Returns:
            dict: Statistics including total jobs, jobs by company, etc.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Total jobs
            cursor.execute("SELECT COUNT(*) as total FROM jobs")
            total = cursor.fetchone()['total']

            # Jobs by company
            cursor.execute("SELECT company, COUNT(*) as count FROM jobs GROUP BY company")
            by_company = {row['company']: row['count'] for row in cursor.fetchall()}

            # Average salary max
            cursor.execute("SELECT AVG(salary_max) as avg_salary FROM jobs WHERE salary_max IS NOT NULL")
            avg_salary = cursor.fetchone()['avg_salary']

            return {
                'total_jobs': total,
                'jobs_by_company': by_company,
                'average_salary_max': avg_salary
            }
