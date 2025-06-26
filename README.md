### 📌 Careerjet Job Scraper

The **Careerjet Job Scraper** is a scraping pipeline built with Scrapy, designed to extract job listings and full job descriptions from [Careerjet Bangladesh](https://www.careerjet.com.bd). It captures both summary and detailed job data, storing results in a structured SQLite database.

Key capabilities include:

* **Dual-Stage Crawling**: One spider scrapes job summaries (title, company, location, salary, URL), while a second spider fetches the corresponding full job descriptions.
* **LLM-Based Enrichment**: A downstream enrichment module uses Cohere's LLM (via LangChain) to extract structured components like responsibilities, requirements, benefits, and compensation from raw job descriptions.
* **Clean Data Storage**: Data flows through validated pipelines into a normalized schema with three tables: `jobs`, `job_description`, and `job_components`.
* **Configurable and Resilient**: Includes retry logic, auto-throttling, randomized delays, and robust error handling. User-agent rotation and caching are also enabled.
* **Minimal Setup, Local Storage**: Easily deployable with a virtual environment, requires only a `.env` file for API credentials, and uses SQLite for local persistence.
