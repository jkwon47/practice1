"""Configuration settings for the job scraper."""
from datetime import datetime, timedelta

# Database settings
DATABASE_PATH = "jobs.db"

# Scraping settings
TARGET_KEYWORDS = ["venture capital", "corporate development"]
EXCLUDED_KEYWORDS = ["associate"]
MIN_SALARY = 200000
DAYS_BACK = 3

# Company configurations
COMPANIES = {
    "google": {
        "name": "Google",
        "careers_url": "https://careers.google.com/jobs/results/",
        "enabled": True
    },
    "meta": {
        "name": "Meta",
        "careers_url": "https://www.metacareers.com/jobs",
        "enabled": True
    },
    "amazon": {
        "name": "Amazon",
        "careers_url": "https://www.amazon.jobs/en/search",
        "enabled": True
    },
    "microsoft": {
        "name": "Microsoft",
        "careers_url": "https://careers.microsoft.com/us/en/search-results",
        "enabled": True
    },
    "nvidia": {
        "name": "NVIDIA",
        "careers_url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite",
        "enabled": True
    },
    "amd": {
        "name": "AMD",
        "careers_url": "https://jobs.amd.com/careers-home/jobs",
        "enabled": True
    }
}

# Request settings
REQUEST_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
REQUEST_DELAY = 2  # seconds between requests to be respectful
