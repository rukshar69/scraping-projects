
# Careerjet Job Scraper

A scalable and configurable Scrapy-based project to extract job listings and full job descriptions from [Careerjet Bangladesh](https://www.careerjet.com.bd). The project stores structured data into a local SQLite database for further analysis and research.

## 📦 Project Structure

```bash
careerjet/
├── spiders/
│   ├── careerjet_crawler.py           # Spider to scrape job listing summaries
│   └── careerjet_description_crawler.py  # Spider to fetch full job descriptions
├── items.py                            # Scraped data schema
├── pipelines.py                        # Cleans and stores items to SQLite
├── middlewares.py                      # Custom user-agent rotation
├── settings.py                         # Project settings
├── requirements.txt                    # Python dependencies
```

## 🚀 Features

* **Multi-stage scraping**:

  * `careerjet_crawler`: Extracts job title, company, location, salary, and job link from 100 pages.
  * `careerjet_description`: Loads job links from DB, fetches full descriptions, and updates statuses.
* **SQLite integration**:

  * Persists job listings and descriptions.
  * Avoids duplicates with unique constraints.
* **Batch-based crawling**:

  * Processes jobs in batches with `crawl_status` control.
* **Test mode support**:

  * Configurable limits for development or test runs.
* **Data normalization**:

  * Salary parsing, title and location cleanup, link normalization.
* **Resilient crawling**:

  * Retry, throttling, and user-agent rotation enabled.

---

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/careerjet-scraper.git
   cd careerjet-scraper
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## ⚙ Usage

### 1. Scrape Job Listings

```bash
scrapy crawl careerjet_crawler
```

Saves data into `careerjet_jobs.db` under `jobs` table.

### 2. Scrape Full Job Descriptions

```bash
scrapy crawl careerjet_description
```

Fetches job descriptions for records where `crawl_status = 'NEW'` in `jobs` table and stores them in `job_description` table.

---

## 🗃 Database Schema

### `jobs` Table

| Field         | Type     | Description                        |
| ------------- | -------- | ---------------------------------- |
| id            | INTEGER  | Auto-increment primary key         |
| title         | TEXT     | Job title                          |
| company       | TEXT     | Company name                       |
| job\_link     | TEXT     | Absolute job URL (unique)          |
| location      | TEXT     | Job location                       |
| salary        | TEXT     | Normalized salary text             |
| page          | INTEGER  | Pagination page number             |
| scraped\_at   | DATETIME | Timestamp of scraping              |
| crawl\_status | TEXT     | `NEW`, `IN_PROGRESS`, `DONE`, etc. |

### `job_description` Table

| Field            | Type    | Description                     |
| ---------------- | ------- | ------------------------------- |
| id               | INTEGER | Auto-increment primary key      |
| job\_link        | TEXT    | Matches `jobs.job_link`, UNIQUE |
| job\_description | TEXT    | Full scraped job description    |
| status           | TEXT    | Status of description crawl defaults to NEW    |

---

## 🧼 Data Pipelines

### `CleaningPipeline`

* Validates title presence
* Normalizes company, location, and salary
* Converts relative URLs to absolute
* Injects `scraped_at` timestamp

### `SQLitePipeline`

* Creates and inserts records into `jobs` table
* Avoids inserting job entries with duplicate `job_link`

### `JobDescriptionPipeline`

* Creates and inserts into `job_description` table
* Marks processed jobs as `DONE` or `NO_DESCRIPTION_FOUND` or error code in `jobs` table

---

## 🕷 Spider Details

### `careerjet_crawler`

* Scrapes pages 1 to 100
* Extracts job summary data like title, compary, salary, etc.

### `careerjet_description`

* Loads job links with `crawl_status = 'NEW'` in batches
* Scrapes full job descriptions from each URL
* Updates crawl status and supports batch limits for testing

---

## ⚙ Configuration Highlights

Defined in `settings.py`:

* **Download delay**: 1.2 seconds, randomized
* **Auto-throttle**: Enabled
* **Retry policy**: Enabled for 3 attempts
* **User-agent rotation**: Enabled via custom middleware
* **Feed export**: CSV output is disabled in favor of SQLite
* **HTTP cache**: Enabled for efficient testing

---

## 📄 Example Query

To view 10 latest scraped jobs with descriptions:

```sql
SELECT j.title, j.company, j.location, d.job_description
FROM jobs j
JOIN job_description d ON j.job_link = d.job_link
ORDER BY j.scraped_at DESC
LIMIT 10;
```

---

## 🧪 Testing

You can test spiders using:

```bash
scrapy crawl careerjet_crawler 
scrapy crawl careerjet_description 
```

---

**Disclaimer:** This project is for educational and research purposes.