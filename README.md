### 📌 Careerjet Job Scraper

The **Careerjet Job Scraper** is a scraping pipeline built with Scrapy, designed to extract job listings and full job descriptions from [Careerjet Bangladesh](https://www.careerjet.com.bd). It captures both summary and detailed job data, storing results in a structured SQLite database.

Key capabilities include:

* **Dual-Stage Crawling**: One spider scrapes job summaries (title, company, location, salary, URL), while a second spider fetches the corresponding full job descriptions.
* **LLM-Based Enrichment**: A downstream enrichment module uses Cohere's LLM (via LangChain) to extract structured components like responsibilities, requirements, benefits, and compensation from raw job descriptions.
* **Clean Data Storage**: Data flows through validated pipelines into a normalized schema with three tables: `jobs`, `job_description`, and `job_components`.
* **Configurable and Resilient**: Includes retry logic, auto-throttling, randomized delays, and robust error handling. User-agent rotation and caching are also enabled.
* **Minimal Setup, Local Storage**: Easily deployable with a virtual environment, requires only a `.env` file for API credentials, and uses SQLite for local persistence.

---

### 📌 FutureTools Scraper

The **FutureTools Scraper** is a Scrapy-powered crawler designed to extract structured product metadata from [FutureTools.io](https://www.futuretools.io). It enables automated harvesting of AI tool listings, metadata, and status tracking using an SQLite-backed pipeline.

Key capabilities include:

* **Two-Stage Workflow**: The `tool_link_spider` collects individual tool page URLs, while the `tool_info_spider` parses each tool's details such as name, description, upvotes, tags, pricing model, and external links.
* **Database-Driven Status Tracking**: A local SQLite database (`ai_tools.db`) tracks each tool's crawl status (`NEW`, `PROCESSING`, `DONE`, or error code), ensuring precise progress control and resumption.
* **Smart Retry with Rate Limit Handling**: A custom middleware honors `Retry-After` headers for 429 responses, introducing async-safe delays to avoid overloading the target server.
* **User-Agent Rotation & Throttling**: Randomized user-agent selection and Scrapy’s auto-throttle help minimize detection and respect server response load.
* **CLI & Script Integration**: Includes Bash and Python scripts (`run_crawler_loop.sh`, `check_new_links.py`, `change_status.py`) for automated, batched crawling with log cleanup and exit control.
