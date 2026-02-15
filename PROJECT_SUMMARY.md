# Project Summary: Job Scraper for VC & Corporate Development Positions

**Created**: February 15, 2026
**Status**: Template Framework Complete
**Branch**: `claude/job-scraper-project-RuaH8`

---

## 🎯 Project Overview

A modular Python-based web scraping system designed to automatically discover and track high-paying venture capital and corporate development positions at major tech companies.

### Target Companies (6)
- Google
- Meta (Facebook)
- Amazon
- Microsoft
- NVIDIA
- AMD

### Search Criteria
- **Keywords**: "venture capital" OR "corporate development"
- **Exclusions**: Jobs with "associate" in title
- **Salary**: Minimum max salary > $200,000
- **Recency**: Posted within last 3 days
- **Storage**: SQLite database with duplicate prevention

---

## ✅ Implemented Features

### 1. Database Management
**Status**: ✅ Complete

- **SQLite integration** with full CRUD operations
- **Automatic duplicate prevention** using unique job IDs
- **Optimized queries** with strategic indexes (company, date, salary)
- **Data persistence** across scraping sessions
- **Statistics tracking** (total jobs, jobs per company, average salary)

**Files**:
- `database/models.py` - Job dataclass with built-in filtering logic
- `database/manager.py` - Database operations with context managers
- `database/__init__.py` - Package exports

### 2. Modular Scraper Architecture
**Status**: ✅ Framework complete, ⚠️ Scrapers need customization

- **Base scraper class** with common functionality (HTTP requests, rate limiting, error handling)
- **Company-specific scrapers** for each target company
- **Template method pattern** for extensibility
- **Automatic logging** of all scraping activities
- **Rate limiting** (2-second delays between requests)
- **User agent spoofing** for better compatibility

**Files**:
- `scrapers/base.py` - Abstract base class
- `scrapers/google.py` - Google careers scraper template
- `scrapers/meta.py` - Meta careers scraper template
- `scrapers/amazon.py` - Amazon careers scraper template
- `scrapers/microsoft.py` - Microsoft careers scraper template
- `scrapers/nvidia.py` - NVIDIA careers scraper template
- `scrapers/amd.py` - AMD careers scraper template
- `scrapers/__init__.py` - Package exports

### 3. Intelligent Filtering System
**Status**: ✅ Complete

- **Multi-criteria filtering**: salary, keywords, date, exclusions
- **Keyword matching** in both title and description
- **Case-insensitive** keyword search
- **Date-based filtering** with configurable lookback period
- **Salary range validation**

**Files**:
- `utils/filters.py` - JobFilter class with static methods
- `database/models.py` - Job.meets_criteria() method

### 4. Orchestration & Workflow
**Status**: ✅ Complete

- **Single entry point** (`main.py`) for easy execution
- **Automatic initialization** of all components
- **Sequential scraping** of all companies
- **Batch processing** of jobs
- **Comprehensive logging** to console and file
- **Summary statistics** after each run

**Files**:
- `main.py` - JobScraperOrchestrator class and main() function

### 5. Configuration Management
**Status**: ✅ Complete

- **Centralized configuration** file
- **Easy customization** of search criteria
- **Company enable/disable** toggles
- **URL management** for all companies
- **Request settings** (timeout, user agent, delays)

**Files**:
- `config.py` - All configuration constants

### 6. Error Handling & Logging
**Status**: ✅ Complete

- **Comprehensive logging** with timestamps and log levels
- **Console output** for real-time monitoring
- **File logging** for historical records
- **Error recovery** - failures in one scraper don't stop others
- **Graceful degradation** - continues on errors

**Implementation**: Throughout all modules

### 7. Documentation
**Status**: ✅ Complete

- **Detailed README** with usage instructions
- **Code comments** explaining complex logic
- **Type hints** for better code clarity
- **Docstrings** for all classes and methods
- **This summary document**

**Files**:
- `README.md` - Comprehensive project documentation
- `PROJECT_SUMMARY.md` - This file

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Total Files | 18 |
| Total Lines of Code | ~1,822 |
| Python Modules | 3 (database, scrapers, utils) |
| Company Scrapers | 6 |
| Filter Criteria | 4 |
| Database Tables | 1 |
| Database Indices | 3 |
| Git Commits | 2 |

---

## 📁 Complete File Inventory

### Root Level (5 files)
```
main.py              - 186 lines - Entry point and orchestration
config.py            - 42 lines  - Configuration settings
requirements.txt     - 12 lines  - Python dependencies
README.md            - 516 lines - Project documentation
.gitignore           - 35 lines  - Git ignore rules
```

### Database Module (3 files)
```
database/__init__.py  - 5 lines   - Package exports
database/models.py    - 71 lines  - Job data model
database/manager.py   - 204 lines - SQLite operations
```

### Scrapers Module (8 files)
```
scrapers/__init__.py   - 17 lines  - Package exports
scrapers/base.py       - 95 lines  - Base scraper class
scrapers/google.py     - 102 lines - Google template
scrapers/meta.py       - 95 lines  - Meta template
scrapers/amazon.py     - 138 lines - Amazon template
scrapers/microsoft.py  - 121 lines - Microsoft template
scrapers/nvidia.py     - 94 lines  - NVIDIA template
scrapers/amd.py        - 122 lines - AMD template
```

### Utils Module (2 files)
```
utils/__init__.py  - 4 lines  - Package exports
utils/filters.py   - 71 lines - Filtering utilities
```

---

## 🏗️ Architecture & Design Patterns

### 1. Object-Oriented Design
- **Inheritance**: All scrapers extend `BaseScraper`
- **Abstraction**: Abstract base class defines interface
- **Encapsulation**: Each module handles its own responsibilities
- **Polymorphism**: Each scraper implements `scrape()` differently

### 2. Design Patterns Used

**Template Method Pattern**:
```python
class BaseScraper:
    def run(self):  # Template method
        self.logger.info(f"Starting scrape for {self.company_name}")
        jobs = self.scrape()  # Calls subclass implementation
        return jobs
```

**Context Manager Pattern**:
```python
class DatabaseManager:
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
```

**Factory Pattern** (simplified):
```python
def _get_scraper_class(self, company_key: str):
    scraper_map = {
        'google': GoogleScraper,
        'meta': MetaScraper,
        # ...
    }
    return scraper_map.get(company_key)
```

### 3. Separation of Concerns

| Concern | Module | Responsibility |
|---------|--------|----------------|
| Data Model | `database/models.py` | Job structure and validation |
| Data Persistence | `database/manager.py` | Database operations |
| Web Scraping | `scrapers/*.py` | HTML fetching and parsing |
| Filtering | `utils/filters.py` | Job filtering logic |
| Configuration | `config.py` | Settings management |
| Orchestration | `main.py` | Workflow coordination |

---

## 🔄 Data Flow

```
User runs main.py
       ↓
JobScraperOrchestrator initializes
       ↓
Creates 6 scraper instances (Google, Meta, etc.)
       ↓
For each company:
   ├─> Scraper.run() called
   ├─> fetch_page() downloads HTML
   ├─> parse_html() parses with BeautifulSoup
   ├─> scrape() extracts job data
   └─> Returns List[Job]
       ↓
All jobs collected (List[Job])
       ↓
JobFilter.filter_jobs() applied
   ├─> Check salary_max > $200k
   ├─> Check posted_date within 3 days
   ├─> Check no "associate" in title
   └─> Check has "VC" or "corp dev" keywords
       ↓
Filtered jobs (List[Job])
       ↓
DatabaseManager.add_jobs_batch()
   ├─> For each job:
   │   ├─> Check if job_id exists
   │   ├─> If new: INSERT
   │   └─> If duplicate: SKIP
   └─> Return count of new jobs
       ↓
Print summary statistics
       ↓
Complete!
```

---

## ⚙️ Technical Details

### Dependencies
```
requests==2.31.0       # HTTP client for web requests
beautifulsoup4==4.12.0 # HTML parsing
lxml==5.1.0           # XML/HTML parser backend
```

### Database Schema
```sql
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,           -- MD5 hash of company+URL
    company TEXT NOT NULL,              -- Company name
    title TEXT NOT NULL,                -- Job title
    location TEXT NOT NULL,             -- Job location
    salary_min REAL,                    -- Minimum salary (nullable)
    salary_max REAL,                    -- Maximum salary (nullable)
    posted_date TEXT NOT NULL,          -- ISO format date
    url TEXT NOT NULL,                  -- Job posting URL
    description TEXT,                   -- Full description (nullable)
    scraped_at TEXT NOT NULL,           -- When we scraped it
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_company ON jobs(company);
CREATE INDEX idx_posted_date ON jobs(posted_date);
CREATE INDEX idx_salary_max ON jobs(salary_max);
```

### Filtering Logic
A job passes filters if ALL of these are true:
```python
1. salary_max is not None AND salary_max > 200000
2. (datetime.now() - posted_date).days <= 3
3. "associate" NOT IN title.lower()
4. ("venture capital" IN search_text) OR ("corporate development" IN search_text)
   where search_text = title.lower() + " " + description.lower()
```

---

## 🚧 Current Limitations

### 1. Scraper Templates Are Not Functional
**Issue**: Company scrapers are templates that need customization.

**Why**:
- Career pages use different HTML structures
- Many sites use JavaScript rendering (requires Selenium)
- Page structures change frequently
- Some companies may use APIs instead

**What needs to be done**:
- Inspect each company's actual careers page
- Update CSS selectors and parsing logic
- Add Selenium if JavaScript rendering needed
- Test with real data

### 2. Salary Data Often Unavailable
**Issue**: Most companies don't list salaries publicly.

**Impact**: Many jobs will be filtered out even if they match other criteria.

**Solutions**:
- Integrate with salary databases (Glassdoor, Levels.fyi)
- Focus on companies that do list salaries
- Make salary filtering optional
- Use external data enrichment

### 3. No JavaScript Rendering
**Issue**: Many career pages load content dynamically with JavaScript.

**Impact**: BeautifulSoup alone can't see JavaScript-loaded content.

**Solution**: Add Selenium or Playwright for browser automation.

### 4. Single-Threaded Execution
**Issue**: Scrapers run sequentially, not in parallel.

**Impact**: Slower total execution time.

**Solution**: Use ThreadPoolExecutor or asyncio for concurrent scraping.

### 5. No Retry Logic
**Issue**: Network failures cause scraper to fail for that company.

**Impact**: Missed jobs on temporary network issues.

**Solution**: Add retry logic with exponential backoff.

---

## 🎯 Next Steps (Prioritized)

### PHASE 1: Make It Work (Critical)

#### 1.1 Customize Google Scraper
**Priority**: HIGH
**Effort**: 2-4 hours
**Tasks**:
- [ ] Visit https://careers.google.com/jobs/results/
- [ ] Inspect HTML structure (F12 Developer Tools)
- [ ] Check if JavaScript rendering is needed
- [ ] Update CSS selectors in `google.py`
- [ ] Test with real data
- [ ] Handle pagination if needed

#### 1.2 Add Selenium Support
**Priority**: HIGH
**Effort**: 3-5 hours
**Tasks**:
- [ ] Install Selenium: `pip install selenium webdriver-manager`
- [ ] Create `SeleniumBaseScraper` class
- [ ] Update scrapers to inherit from new base class
- [ ] Test JavaScript rendering
- [ ] Add headless mode option

#### 1.3 Implement One Working Scraper
**Priority**: HIGH
**Effort**: 4-6 hours
**Recommendation**: Start with Amazon or Microsoft (often have better structured pages)
**Tasks**:
- [ ] Choose one company
- [ ] Fully implement scraper
- [ ] Test end-to-end
- [ ] Verify jobs are saved to database
- [ ] Document the process

### PHASE 2: Enhance Reliability (Important)

#### 2.1 Add Retry Logic
**Priority**: MEDIUM
**Effort**: 1-2 hours
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def fetch_page(self, url):
    # existing code
```

#### 2.2 Improve Error Handling
**Priority**: MEDIUM
**Effort**: 2-3 hours
**Tasks**:
- [ ] Add try-except blocks for missing data fields
- [ ] Handle network timeouts gracefully
- [ ] Log detailed error information
- [ ] Continue on individual job parsing failures

#### 2.3 Add Data Validation
**Priority**: MEDIUM
**Effort**: 1-2 hours
**Tasks**:
- [ ] Validate URLs are valid
- [ ] Check salary ranges are reasonable
- [ ] Ensure dates are parseable
- [ ] Validate job IDs are unique

### PHASE 3: Add Features (Nice to Have)

#### 3.1 Email Notifications
**Priority**: LOW
**Effort**: 2-3 hours
**Tasks**:
- [ ] Set up SMTP configuration
- [ ] Create email template
- [ ] Send summary email after each run
- [ ] Include links to new jobs

#### 3.2 Parallel Scraping
**Priority**: LOW
**Effort**: 2-3 hours
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=6) as executor:
    futures = [executor.submit(scraper.run) for scraper in scrapers.values()]
    results = [future.result() for future in futures]
```

#### 3.3 Web Dashboard
**Priority**: LOW
**Effort**: 8-12 hours
**Tasks**:
- [ ] Create Flask/FastAPI app
- [ ] Build HTML templates
- [ ] Add filtering and sorting UI
- [ ] Display job statistics

### PHASE 4: Production Ready (Advanced)

#### 4.1 Scheduled Execution
**Priority**: LOW
**Effort**: 1 hour
**Options**:
- Cron job (Linux/Mac)
- Windows Task Scheduler
- Cloud Functions (AWS Lambda, Google Cloud Functions)

#### 4.2 Monitoring & Alerting
**Priority**: LOW
**Effort**: 4-6 hours
**Tasks**:
- [ ] Track scraper success rates
- [ ] Monitor database growth
- [ ] Alert on consecutive failures
- [ ] Create health check endpoint

#### 4.3 API Integration
**Priority**: MEDIUM
**Effort**: Variable (depends on API availability)
**Tasks**:
- [ ] Research which companies offer APIs
- [ ] Implement API clients
- [ ] Replace scrapers with API calls where possible
- [ ] Handle API rate limits

---

## 📝 Testing Recommendations

### Unit Tests
```python
# tests/test_filters.py
def test_job_meets_criteria():
    job = Job(
        job_id="test",
        company="TestCo",
        title="VP Venture Capital",
        salary_max=250000,
        posted_date=datetime.now(),
        # ...
    )
    assert job.meets_criteria(
        min_salary=200000,
        days_back=3,
        target_keywords=["venture capital"],
        excluded_keywords=["associate"]
    )
```

### Integration Tests
```python
# tests/test_database.py
def test_database_duplicate_prevention():
    db = DatabaseManager()
    job = create_test_job()

    # First add should succeed
    assert db.add_job(job) == True

    # Second add should be skipped
    assert db.add_job(job) == False
```

### End-to-End Tests
```python
# tests/test_scraper.py
def test_google_scraper():
    scraper = GoogleScraper("https://careers.google.com/jobs/results/")
    jobs = scraper.run()

    assert len(jobs) > 0
    assert all(isinstance(job, Job) for job in jobs)
    assert all(job.company == "Google" for job in jobs)
```

---

## 🔐 Security & Ethics Considerations

### Web Scraping Ethics
1. **Respect robots.txt**: Check each site's robots.txt file
2. **Rate limiting**: Already implemented (2-second delays)
3. **User agent**: Clearly identify as a scraper
4. **Terms of Service**: Review each company's ToS
5. **Data privacy**: Only collect public job postings

### Security
1. **Input validation**: Validate all scraped data
2. **SQL injection**: Using parameterized queries (✅ implemented)
3. **XSS prevention**: Don't render scraped HTML directly
4. **Secrets management**: Don't hardcode credentials
5. **HTTPS**: Use secure connections

---

## 📚 Learning Resources

### Web Scraping
- BeautifulSoup documentation: https://www.crummy.com/software/BeautifulSoup/
- Selenium documentation: https://selenium-python.readthedocs.io/
- Requests library: https://docs.python-requests.org/

### Database
- SQLite documentation: https://www.sqlite.org/docs.html
- Python sqlite3 module: https://docs.python.org/3/library/sqlite3.html

### Python Best Practices
- PEP 8 Style Guide: https://pep8.org/
- Type hints: https://docs.python.org/3/library/typing.html
- Logging: https://docs.python.org/3/library/logging.html

---

## 🤝 Contributing Guidelines

If you enhance this project:

1. **Follow the existing architecture**
2. **Add type hints** to new functions
3. **Write docstrings** for new classes/methods
4. **Update README.md** with new features
5. **Add logging** for important operations
6. **Test your changes** before committing
7. **Use meaningful commit messages**

---

## 📞 Support & Questions

Common issues and solutions:

| Issue | Solution |
|-------|----------|
| No jobs found | Check URL validity, HTML structure, need for JavaScript rendering |
| Duplicates appearing | Verify job_id generation is consistent |
| Database locked | Close other connections, check file permissions |
| Import errors | Ensure all dependencies installed: `pip install -r requirements.txt` |
| Scraper timeout | Increase `REQUEST_TIMEOUT` in config.py |

---

## 🎓 Summary

This project provides a **solid foundation** for automated job scraping with:

✅ **Clean architecture** - Modular, extensible, maintainable
✅ **Database integration** - Persistent storage with duplicate prevention
✅ **Filtering system** - Multi-criteria job filtering
✅ **Error handling** - Graceful degradation on failures
✅ **Comprehensive logging** - Full visibility into operations
✅ **Documentation** - Detailed README and code comments

⚠️ **Requires customization** - Company scrapers need updating for actual websites

**Next immediate step**: Implement one fully working scraper (recommend starting with Amazon or Microsoft) to validate the entire pipeline, then expand to other companies.

---

**Last Updated**: February 15, 2026
**Git Branch**: `claude/job-scraper-project-RuaH8`
**Commits**: 2
