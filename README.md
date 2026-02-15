# Job Scraper for Venture Capital & Corporate Development Positions

A Python-based job scraper that monitors career pages of major tech companies (Google, Meta, Amazon, Microsoft, NVIDIA, AMD) for high-paying venture capital and corporate development positions.

## 📋 What We've Built

This project is a **modular, extensible job scraping system** designed to automatically find and track high-paying venture capital and corporate development positions at major tech companies.

### Current Status: Template Implementation

The project includes a **complete, working framework** with:
- ✅ Modular architecture with base classes and inheritance
- ✅ Database integration with duplicate prevention
- ✅ Comprehensive filtering system
- ✅ Logging and error handling
- ✅ Configuration management
- ⚠️ Template scrapers that need customization for actual company websites

**Note**: The company-specific scrapers are templates that demonstrate the architecture. To actually scrape jobs, you'll need to customize them based on each company's current website structure (see [Customization](#customization-guide) section).

## Features

- **Multi-company monitoring**: Tracks jobs from 6 major tech companies
- **Keyword filtering**: Searches for "venture capital" OR "corporate development" positions
- **Title exclusion**: Filters out jobs with "associate" in the title
- **Salary filtering**: Only includes jobs with maximum salary above $200,000
- **Recency filtering**: Tracks jobs posted within the last 3 days
- **Duplicate prevention**: Uses SQLite database to avoid storing duplicate jobs
- **Comprehensive logging**: Logs all activities to both console and file

## 🔄 How It Works

Here's the complete workflow when you run `python main.py`:

```
1. Initialize
   └─> Create DatabaseManager instance
   └─> Initialize all company scrapers
   └─> Load configuration from config.py

2. Scrape Jobs (for each company)
   └─> GoogleScraper.run()
       ├─> Fetch careers page HTML
       ├─> Parse HTML with BeautifulSoup
       ├─> Extract job listings
       ├─> Create Job objects
       └─> Return list of jobs
   └─> (Repeat for Meta, Amazon, Microsoft, NVIDIA, AMD)

3. Filter Jobs
   └─> For each job:
       ├─> Check salary_max > $200,000
       ├─> Check posted within last 3 days
       ├─> Check title doesn't contain "associate"
       ├─> Check title/description contains "venture capital" OR "corporate development"
       └─> Keep only if ALL criteria pass

4. Save to Database
   └─> For each filtered job:
       ├─> Check if job_id exists in database
       ├─> If new: INSERT into jobs table
       └─> If duplicate: Skip

5. Print Summary
   └─> Total jobs scraped
   └─> Jobs meeting criteria
   └─> New jobs added
   └─> Database statistics
```

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

## 📁 Project Structure

```
practice1/
├── main.py                 # Entry point and orchestration
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
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

## 📄 Detailed File Descriptions

### Core Files

#### `main.py` (Entry Point)
**Purpose**: Orchestrates the entire job scraping workflow.

**Key Components**:
- `JobScraperOrchestrator` class: Main controller that manages all scrapers
- `scrape_all_companies()`: Iterates through all enabled companies and runs their scrapers
- `filter_jobs()`: Applies all filtering criteria to scraped jobs
- `save_jobs()`: Stores qualifying jobs in the database
- `print_summary()`: Displays statistics about the scraping session

**Usage**: Run with `python main.py`

**What it does**:
1. Initializes database connection
2. Creates scraper instances for each company
3. Scrapes jobs from all companies in sequence
4. Filters results based on keywords, salary, and date criteria
5. Saves new jobs to database (skipping duplicates)
6. Prints detailed statistics

---

#### `config.py` (Configuration)
**Purpose**: Centralized configuration for easy customization.

**Settings**:
- `TARGET_KEYWORDS`: List of keywords to search for in job titles/descriptions
  - Default: `["venture capital", "corporate development"]`
- `EXCLUDED_KEYWORDS`: Keywords that disqualify a job
  - Default: `["associate"]`
- `MIN_SALARY`: Minimum salary maximum threshold
  - Default: `200000` (jobs must pay over $200k max)
- `DAYS_BACK`: How many days back to search
  - Default: `3` (only jobs posted in last 3 days)
- `COMPANIES`: Dictionary of company configurations with URLs
- `REQUEST_TIMEOUT`: HTTP request timeout (30 seconds)
- `USER_AGENT`: Browser user agent string for requests
- `REQUEST_DELAY`: Delay between requests (2 seconds) for polite scraping

**How to customize**: Edit this file to change filtering criteria or add companies.

---

### Database Module (`database/`)

#### `database/models.py`
**Purpose**: Defines the Job data model and filtering logic.

**Key Class**: `Job` (dataclass)
- Represents a single job posting with all metadata
- **Attributes**:
  - `job_id`: Unique identifier (MD5 hash of company + URL)
  - `company`: Company name (e.g., "Google", "Meta")
  - `title`: Job title
  - `location`: Job location
  - `salary_min`, `salary_max`: Salary range (if available)
  - `posted_date`: When job was posted
  - `url`: Link to job posting
  - `description`: Full job description text
  - `scraped_at`: Timestamp when we scraped it

**Key Method**: `meets_criteria()`
- Checks if job passes all filters
- Returns `True` only if job matches ALL requirements:
  - Salary max > minimum threshold
  - Posted within date range
  - No excluded keywords in title
  - Has at least one target keyword in title or description

---

#### `database/manager.py`
**Purpose**: Handles all SQLite database operations.

**Key Class**: `DatabaseManager`

**Methods**:
- `init_database()`: Creates tables and indices if they don't exist
- `job_exists(job_id)`: Checks if job is already in database (prevents duplicates)
- `add_job(job)`: Adds single job to database
- `add_jobs_batch(jobs)`: Efficiently adds multiple jobs
- `get_all_jobs()`: Retrieves all stored jobs
- `get_jobs_by_company(company)`: Gets jobs for specific company
- `get_stats()`: Returns statistics (total jobs, jobs per company, avg salary)

**Database Schema**:
```sql
CREATE TABLE jobs (
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
```

**Indices** (for performance):
- `idx_company`: Fast company lookups
- `idx_posted_date`: Fast date filtering
- `idx_salary_max`: Fast salary filtering

---

### Scrapers Module (`scrapers/`)

#### `scrapers/base.py`
**Purpose**: Abstract base class that all company scrapers inherit from.

**Key Class**: `BaseScraper` (ABC)

**Provides**:
- `fetch_page(url)`: Downloads HTML with error handling and rate limiting
- `parse_html(html)`: Parses HTML using BeautifulSoup
- `run()`: Template method that calls `scrape()` with error handling

**Abstract Method**: `scrape()` - Must be implemented by each company scraper

**Features**:
- Automatic user agent injection
- Request timeout handling
- Rate limiting (2 second delay between requests)
- Comprehensive logging
- Error recovery

---

#### Company Scrapers (`scrapers/*.py`)
**Files**: `google.py`, `meta.py`, `amazon.py`, `microsoft.py`, `nvidia.py`, `amd.py`

**Purpose**: Each implements company-specific scraping logic.

**Current Status**: ⚠️ **Template implementations**

Each scraper:
- Extends `BaseScraper`
- Implements `scrape()` method
- Parses company-specific HTML structure
- Extracts: title, location, URL, salary (if available), posted date, description
- Generates unique job IDs using MD5 hashing
- Includes helper methods for parsing salary and dates

**Why templates?**:
- Career page structures change frequently
- Many sites use JavaScript rendering (need Selenium)
- Some companies use APIs instead of scrapable HTML
- Each requires customization based on current site structure

**Example structure**:
```python
class GoogleScraper(BaseScraper):
    def __init__(self, careers_url: str):
        super().__init__("Google", careers_url)

    def scrape(self) -> List[Job]:
        # Fetch page
        # Parse HTML
        # Extract job listings
        # Return list of Job objects
        pass
```

---

### Utils Module (`utils/`)

#### `utils/filters.py`
**Purpose**: Utility functions for filtering jobs.

**Key Class**: `JobFilter`

**Static Methods**:
- `filter_jobs()`: Main filtering function that applies all criteria
- `has_target_keywords()`: Checks if text contains target keywords
- `has_excluded_keywords()`: Checks if text contains excluded keywords
- `is_recent()`: Checks if job is within date range

**Why separate from models?**:
- Separation of concerns
- Reusable across different contexts
- Easier to test independently

---

### Supporting Files

#### `requirements.txt`
**Purpose**: Lists Python dependencies for easy installation.

**Dependencies**:
- `requests`: HTTP library for making web requests
- `beautifulsoup4`: HTML parsing library
- `lxml`: Fast XML/HTML parser (used by BeautifulSoup)

**Commented optional dependencies**:
- `selenium`: For JavaScript-rendered pages
- `scrapy`: Advanced scraping framework
- Development tools (pytest, black, pylint)

**Install**: `pip install -r requirements.txt`

---

#### `.gitignore`
**Purpose**: Tells Git which files to ignore.

**Excludes**:
- Python cache files (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- Database files (`*.db`, `*.sqlite`)
- Log files (`*.log`)
- IDE settings (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`)
- Environment variables (`.env`)

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

## 🚀 Next Steps for Production

To make this scraper fully functional, here's what needs to be done:

### Phase 1: Make Scrapers Functional (Required)

Each company scraper needs customization based on their actual website:

1. **Inspect the career pages**:
   ```bash
   # Visit each URL and inspect the HTML structure
   - https://careers.google.com/jobs/results/
   - https://www.metacareers.com/jobs
   - https://www.amazon.jobs/en/search
   # etc.
   ```

2. **Update HTML selectors** in each scraper:
   - Find the correct CSS classes/IDs for job listings
   - Update parsing logic in `_parse_job_listing()` methods
   - Test with real data

3. **Add JavaScript rendering** (if needed):
   ```bash
   pip install selenium webdriver-manager
   ```

   Then modify scrapers to use Selenium for JavaScript-heavy sites.

4. **Implement salary parsing**:
   - Most companies don't list salaries publicly
   - Consider integrating with Levels.fyi or Glassdoor APIs
   - Or focus on companies that do list salaries

### Phase 2: Enhance Reliability (Recommended)

1. **Add robust error handling**:
   - Network timeouts
   - Rate limiting responses
   - Invalid HTML structure
   - Missing data fields

2. **Implement retry logic**:
   ```python
   from tenacity import retry, stop_after_attempt, wait_exponential

   @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
   def fetch_page(self, url):
       # existing code
   ```

3. **Add data validation**:
   - Verify job URLs are valid
   - Check salary ranges make sense
   - Validate dates are parseable

### Phase 3: Production Features (Optional)

1. **Email notifications**:
   ```python
   # Send email when new jobs are found
   import smtplib
   from email.message import EmailMessage
   ```

2. **Web dashboard**:
   - Use Flask/FastAPI to create a web interface
   - Display jobs in a table
   - Filter and sort capabilities

3. **Scheduled runs**:
   - Set up cron job (Linux/Mac)
   - Use Windows Task Scheduler
   - Or use cloud scheduling (AWS Lambda, Google Cloud Functions)

4. **Advanced filtering**:
   - Location preferences
   - Remote vs. on-site
   - Experience level
   - Skills matching

### Phase 4: Scale & Optimize (Advanced)

1. **Parallel scraping**:
   ```python
   from concurrent.futures import ThreadPoolExecutor

   with ThreadPoolExecutor(max_workers=6) as executor:
       futures = [executor.submit(scraper.run) for scraper in scrapers.values()]
   ```

2. **Caching**:
   - Cache HTTP responses
   - Avoid re-scraping unchanged pages

3. **Monitoring**:
   - Track scraper success rates
   - Alert on failures
   - Monitor database growth

4. **API integration**:
   - Use official APIs where available
   - More reliable than scraping
   - Less likely to break

## 📊 Expected Output

When you run the scraper, you'll see output like:

```
2024-02-15 10:30:00 - __main__ - INFO - Starting job scraper...
2024-02-15 10:30:00 - __main__ - INFO - Target keywords: venture capital, corporate development
2024-02-15 10:30:00 - __main__ - INFO - Excluded keywords: associate
2024-02-15 10:30:00 - __main__ - INFO - Minimum salary max: $200,000
2024-02-15 10:30:00 - __main__ - INFO - Days back: 3
============================================================
2024-02-15 10:30:01 - GoogleScraper - INFO - Starting scrape for Google
2024-02-15 10:30:01 - GoogleScraper - INFO - Fetching https://careers.google.com/jobs/results/
2024-02-15 10:30:03 - GoogleScraper - INFO - Found 12 jobs for Google
2024-02-15 10:30:03 - MetaScraper - INFO - Starting scrape for Meta
...
============================================================
SCRAPING SUMMARY
============================================================
Total jobs scraped: 45
Jobs matching criteria: 8
New jobs added to database: 5
Duplicate jobs skipped: 3
============================================================
DATABASE STATISTICS
============================================================
Total jobs in database: 23
Jobs by company:
  Google: 8
  Meta: 6
  Amazon: 4
  Microsoft: 3
  NVIDIA: 2
  AMD: 0
Average max salary: $245,000
============================================================
2024-02-15 10:30:15 - __main__ - INFO - Job scraping completed successfully!
```

## 🎯 Quick Start Guide

**Step 1**: Install dependencies
```bash
pip install -r requirements.txt
```

**Step 2**: (Optional) Customize config
```bash
# Edit config.py to change search criteria
nano config.py
```

**Step 3**: Run the scraper
```bash
python main.py
```

**Step 4**: Check the database
```bash
sqlite3 jobs.db
sqlite> SELECT company, title, salary_max FROM jobs ORDER BY salary_max DESC;
```

## 🧪 Testing Individual Components

Test the database:
```python
from database import DatabaseManager
from database.models import Job
from datetime import datetime

# Create test job
db = DatabaseManager()
job = Job(
    job_id="test123",
    company="TestCo",
    title="VP Corporate Development",
    location="San Francisco",
    salary_min=200000,
    salary_max=300000,
    posted_date=datetime.now(),
    url="https://example.com/job"
)

# Add to database
db.add_job(job)

# Verify
stats = db.get_stats()
print(stats)
```

Test filtering:
```python
from utils import JobFilter
from database.models import Job
from datetime import datetime

# Create test job
job = Job(
    job_id="test",
    company="TestCo",
    title="Venture Capital Associate",  # Has "associate"
    location="NYC",
    salary_min=150000,
    salary_max=250000,
    posted_date=datetime.now(),
    url="https://example.com"
)

# Test if it passes filters
passes = job.meets_criteria(
    min_salary=200000,
    days_back=3,
    target_keywords=["venture capital"],
    excluded_keywords=["associate"]
)

print(f"Passes filters: {passes}")  # Should be False (has "associate")
```

## 📈 Project Statistics

- **Total Files**: 18
- **Lines of Code**: ~1,822
- **Modules**: 3 (database, scrapers, utils)
- **Companies Supported**: 6
- **Filter Criteria**: 4 (keywords, exclusions, salary, date)

## License

This project is for educational purposes. Ensure compliance with website Terms of Service before use.
