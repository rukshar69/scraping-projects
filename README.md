
# Careerjet Job Scraper

A scalable and configurable Scrapy-based project to extract job listings and full job descriptions from [Careerjet Bangladesh](https://www.careerjet.com.bd). The project stores structured data into a local SQLite database for further analysis and research.

## 📦 Project Structure

```bash
web-scraper/
├── careerjet/
│   ├── spiders/
│   │   ├── careerjet_crawler.py              # Spider to scrape job listing summaries
│   │   └── careerjet_description_crawler.py  # Spider to fetch full job descriptions
│   ├── items.py                               # Scraped data schema
│   ├── pipelines.py                           # Cleans and stores items to SQLite
│   ├── middlewares.py                         # User-agent rotation
│   ├── settings.py                            # Scrapy configuration
│   └── requirements.txt
├── job_info_extractor_ai/
│   ├── get_job_components.py                  # Extracts structured job components using LLM
│   └── llm_job_description_parser_v2.py       # LangChain + Cohere schema & prompt for extraction
````


## 🚀 Features

### 🌐 Web Crawling (Scrapy)

* `careerjet_crawler`:

  * Scrapes title, company, location, salary, job URL (up to 100 pages).
* `careerjet_description`:

  * Loads job URLs from DB (`crawl_status='NEW'`), scrapes job description, and updates status.

### 🧠 AI-Powered Enrichment

* `job_info_extractor_ai` module:

  * Extracts structured job insights using Cohere's LLM via LangChain.
  * Targets job responsibilities, requirements, company details, benefits, and compensation.
  * Saves enriched data to a third table: `job_components`.

### 🧱 SQLite Storage

* Schema includes:

  * `jobs` (listing metadata)
  * `job_description` (raw description)
  * `job_components` (AI-enriched structured output)

### 🧼 Robust Pipelines

* Input validation, salary normalization, absolute URL conversion
* Duplicate handling and crawl status tracking
* Logging, retrying, and rate limiting for LLM usage

---

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/careerjet-scraper.git
cd web-scraper
```

2. Set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r careerjet/requirements.txt
```

4. Set up API credentials for LLM:

Create a `.env` file in `job_info_extractor_ai/`:

```
COHERE_API_KEY=your-api-key-here
```

---

## ⚙ Usage

### 1. Crawl Job Listings

```bash
cd careerjet
scrapy crawl careerjet_crawler
```

### 2. Crawl Full Job Descriptions

```bash
scrapy crawl careerjet_description
```

### 3. Extract Job Components via AI

```bash
cd ../job_info_extractor_ai
python get_job_components.py
```

---

## 🗃 Database Schema

### `jobs`

| Field         | Type     | Description                        |
| ------------- | -------- | ---------------------------------- |
| id            | INTEGER  | Auto-increment primary key         |
| title         | TEXT     | Job title                          |
| company       | TEXT     | Company name                       |
| job\_link     | TEXT     | Unique job URL                     |
| location      | TEXT     | Job location                       |
| salary        | TEXT     | Salary normalized                  |
| page          | INTEGER  | Page number from listing           |
| scraped\_at   | DATETIME | Timestamp                          |
| crawl\_status | TEXT     | `NEW`, `IN_PROGRESS`, `DONE`, etc. |

### `job_description`

| Field            | Type    | Description                    |
| ---------------- | ------- | ------------------------------ |
| id               | INTEGER | Auto-increment primary key     |
| job\_link        | TEXT    | Foreign key to `jobs` (unique) |
| job\_description | TEXT    | Full job description           |
| status           | TEXT    | `NEW`, `IN_PROGRESS`, `DONE`   |

### `job_components`

| Field                 | Type     | Description                     |
| --------------------- | -------- | ------------------------------- |
| id                    | INTEGER  | Auto-increment primary key      |
| job\_link             | TEXT     | Foreign key to `jobs` (unique)  |
| job\_responsibilities | TEXT     | Responsibilities section        |
| job\_requirements     | TEXT     | Requirements section            |
| company\_name         | TEXT     | Name extracted from description |
| company\_address      | TEXT     | Address/location if available   |
| application\_email    | TEXT     | Email to apply                  |
| benefits              | TEXT     | Benefits offered                |
| compensation          | TEXT     | Compensation/salary info        |
| extracted\_at         | DATETIME | Timestamp of AI extraction      |

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

To test all stages:

```bash
# Scrapy spiders (no log)
scrapy crawl careerjet_crawler --nolog
scrapy crawl careerjet_description --nolog

# Job enrichment
python get_job_components.py
```

---

**Disclaimer:** This project is for educational and research purposes.