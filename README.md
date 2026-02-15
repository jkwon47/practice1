# Job Scraper for Venture Capital & Corporate Development Positions

A Python-based job scraper that monitors career pages of major tech companies (Google, Meta, Amazon, Microsoft, NVIDIA, AMD) for high-paying venture capital and corporate development positions.

## Features

- **Multi-company monitoring**: Tracks jobs from 6 major tech companies
- **Keyword filtering**: Searches for "venture capital" OR "corporate development" positions
- **Title exclusion**: Filters out jobs with "associate" in the title
- **Salary filtering**: Only includes jobs with maximum salary above $200,000
- **Recency filtering**: Tracks jobs posted within the last 3 days
- **Duplicate prevention**: Uses SQLite database to avoid storing duplicate jobs
- **Comprehensive logging**: Logs all activities to both console and file

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd practice1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:
```bash
python main.py
```

The scraper will:
1. Scrape job listings from all enabled companies
2. Filter jobs based on criteria
3. Store new jobs in SQLite database (`jobs.db`)
4. Print summary statistics

## Configuration

Edit `config.py` to customize:

- `TARGET_KEYWORDS`: Keywords to search for (default: ["venture capital", "corporate development"])
- `EXCLUDED_KEYWORDS`: Keywords to exclude (default: ["associate"])
- `MIN_SALARY`: Minimum maximum salary threshold (default: 200000)
- `DAYS_BACK`: Maximum days since posting (default: 3)
- `COMPANIES`: Enable/disable specific companies or update URLs

## Project Structure

```
practice1/
├── main.py                 # Entry point and orchestration
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── database/             # Database management
│   ├── __init__.py
│   ├── models.py         # Job data model
│   └── manager.py        # SQLite database operations
├── scrapers/             # Company-specific scrapers
│   ├── __init__.py
│   ├── base.py          # Base scraper class
│   ├── google.py
│   ├── meta.py
│   ├── amazon.py
│   ├── microsoft.py
│   ├── nvidia.py
│   └── amd.py
└── utils/               # Utility functions
    ├── __init__.py
    └── filters.py       # Job filtering logic
```

## Database Schema

The SQLite database (`jobs.db`) contains a single `jobs` table:

- `job_id` (TEXT, PRIMARY KEY): Unique job identifier
- `company` (TEXT): Company name
- `title` (TEXT): Job title
- `location` (TEXT): Job location
- `salary_min` (REAL): Minimum salary (if available)
- `salary_max` (REAL): Maximum salary
- `posted_date` (TEXT): When the job was posted
- `url` (TEXT): Link to job posting
- `description` (TEXT): Job description
- `scraped_at` (TEXT): When the job was scraped
- `created_at` (TEXT): When the record was created

## Important Notes

### Scraper Limitations

The scrapers in this project are **template implementations** designed to demonstrate the structure. Real-world usage requires customization because:

1. **Dynamic Content**: Many career pages use JavaScript to load content dynamically
2. **Changing Structure**: Companies frequently update their career page layouts
3. **API Access**: Some companies may offer APIs that are more reliable than scraping
4. **Rate Limiting**: Career pages may have rate limiting or bot protection

### Recommendations for Production Use

For production deployment, consider:

1. **Use Selenium/Playwright**: For JavaScript-rendered pages
   ```bash
   pip install selenium webdriver-manager
   ```

2. **Respect robots.txt**: Check each company's robots.txt file

3. **Add delays**: Implement respectful rate limiting (already included in base scraper)

4. **API Integration**: Check if companies offer official APIs:
   - Google: May have Greenhouse API integration
   - Meta: Check for official careers API
   - Amazon: Look for AWS Jobs API
   - Microsoft: May have programmatic access
   - NVIDIA/AMD: Often use Workday APIs

5. **Error Handling**: Enhance error handling for network issues

6. **Proxy Rotation**: For large-scale scraping

7. **Salary Data**: Many companies don't list salaries publicly. Consider:
   - Using third-party salary databases
   - Integrating with Glassdoor/Levels.fyi APIs
   - Manual enrichment

### Legal Considerations

- Ensure compliance with each website's Terms of Service
- Respect rate limits and robots.txt
- Don't overload servers with requests
- Consider using official APIs when available

## Customization Guide

### Adding a New Company

1. Create a new scraper in `scrapers/`:
```python
from .base import BaseScraper
from database.models import Job

class NewCompanyScraper(BaseScraper):
    def __init__(self, careers_url: str):
        super().__init__("NewCompany", careers_url)

    def scrape(self) -> List[Job]:
        # Implement scraping logic
        pass
```

2. Add to `config.py`:
```python
COMPANIES = {
    # ... existing companies ...
    "newcompany": {
        "name": "NewCompany",
        "careers_url": "https://careers.newcompany.com",
        "enabled": True
    }
}
```

3. Update `scrapers/__init__.py` and `main.py`

### Modifying Filters

Edit `config.py`:
```python
TARGET_KEYWORDS = ["venture capital", "corporate development", "M&A"]
EXCLUDED_KEYWORDS = ["associate", "junior", "intern"]
MIN_SALARY = 250000  # Increase minimum
DAYS_BACK = 7  # Extend to 7 days
```

## Scheduling

To run automatically, use cron (Linux/Mac) or Task Scheduler (Windows):

### Linux/Mac (cron)
```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/practice1 && python main.py
```

### Windows (Task Scheduler)
Create a scheduled task to run `python main.py` at desired intervals.

## Logging

Logs are written to:
- Console (stdout)
- `job_scraper.log` file

## Database Queries

Query the database directly:
```python
from database import DatabaseManager

db = DatabaseManager()

# Get all jobs
jobs = db.get_all_jobs()

# Get jobs by company
google_jobs = db.get_jobs_by_company("Google")

# Get statistics
stats = db.get_stats()
```

## Troubleshooting

### No jobs found
- Check that company URLs are still valid
- Verify HTML structure hasn't changed
- Check if JavaScript rendering is needed
- Review logs for errors

### Duplicate jobs
- The database prevents duplicates by job_id
- If getting duplicates, check job_id generation logic

### Missing salary data
- Many companies don't list salaries publicly
- Consider integrating external salary data sources

## Contributing

Feel free to submit pull requests to:
- Add new company scrapers
- Improve filtering logic
- Enhance error handling
- Add tests

## License

This project is for educational purposes. Ensure compliance with website Terms of Service before use.
