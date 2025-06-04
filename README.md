
# Careerjet Job Scraper

A scalable and configurable Scrapy-based crawler for extracting job listings from [Careerjet Bangladesh](https://www.careerjet.com.bd). This project collects job data including title, company, location, salary, job link, and the page number from which it was scraped. The project gathers job details and stores them in a local SQLite database.

## 📦 Project Structure

```bash
careerjet/
├── spiders/
│   └── careerjet_crawler.py  # Main spider to crawl job listings
├── items.py                  # Defines scraped data schema
├── pipelines.py              # Cleans and normalizes scraped data
├── middlewares.py           # Custom user-agent rotation middleware
├── settings.py              # Project settings and configurations
├── requirements.txt         # Dependencies
```

## 🚀 Features

- Scrapes up to 100 pages of job listings.
- Extracts job title, company, location, salary, and job links.
- Cleans and normalizes salary, company, and location fields.
- Adds scrape timestamp to each item.
- Robust retry and delay settings for respectful crawling.
- Rotates user-agents per request to avoid blocks.
- Persists job data in a local SQLite database `(careerjet_jobs.db)`.

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

## ⚙️ Usage

Run the spider with:

```bash
scrapy crawl careerjet_crawler
```

This will store the extracted job listings in a local SQLite database file: `careerjet_jobs.db`.

## 💾 Database Schema
The SQLite table jobs includes:

| Field         | Type     | Description                |
| ------------- | -------- | -------------------------- |
| id            | INTEGER  | Auto-increment primary key |
| title         | TEXT     | Job title                  |
| company       | TEXT     | Company name               |
| job\_link     | TEXT     | Absolute job URL (unique)  |
| location      | TEXT     | Job location               |
| salary        | TEXT     | Normalized salary text     |
| page          | INTEGER  | Pagination page number     |
| scraped\_at   | DATETIME | Timestamp of scraping      |
| crawl\_status | TEXT     | Default status = 'NEW'     |


## 🧼 Data Pipeline

The `CleaningPipeline` handles:

- Title validation
- Company and location formatting
- Salary parsing and normalization
- Absolute URL formatting for job links
- Timestamp injection (`scraped_at`)

## 🕵️ Spider Details

Located in `spiders/careerjet_crawler.py`, this spider:

- Starts from the first page and paginates up to page 100.
- Logs the parsing status for each page.
- Skips pages without job data.

## ⚙️ Configuration Highlights

Defined in `settings.py`:

- **Throttling & Delay**: `DOWNLOAD_DELAY=1.2`, `AUTOTHROTTLE_ENABLED=True`
- **Retry**: Retries 3 times for HTTP error codes like 500, 503, 429, etc.
- **User-Agent Rotation**: Handled by custom middleware

## 📄 Output Example

| title             | company    | job_link                          | location | salary | page | scraped_at         |
|------------------|------------|-----------------------------------|----------|--------|------|--------------------|
| Software Engineer| ABC Ltd.   | https://careerjet.com.bd/job12345 | Dhaka    | 50000  | 1    | 2025-06-01 15:30   |

## 🧪 Testing

To test locally with HTTP caching enabled:

```bash
scrapy crawl careerjet_crawler --nolog
```

---

**Disclaimer:** This project is for educational and research purposes.