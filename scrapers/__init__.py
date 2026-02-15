"""Scrapers package for job scraper."""
from .base import BaseScraper
from .google import GoogleScraper
from .meta import MetaScraper
from .amazon import AmazonScraper
from .microsoft import MicrosoftScraper
from .nvidia import NVIDIAScraper
from .amd import AMDScraper

__all__ = [
    'BaseScraper',
    'GoogleScraper',
    'MetaScraper',
    'AmazonScraper',
    'MicrosoftScraper',
    'NVIDIAScraper',
    'AMDScraper'
]
