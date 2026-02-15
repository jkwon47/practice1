"""Database package for job scraper."""
from .manager import DatabaseManager
from .models import Job

__all__ = ['DatabaseManager', 'Job']
