# FutureTools Scraper

A Scrapy project to extract detailed AI tool information from [FutureTools.io](https://www.futuretools.io). This project collects structured tool metadata and manages crawling status using a local SQLite database, with custom retry logic, auto-throttling, and CLI-based control.

---

## 📦 Project Structure

```bash
futuretools/
├── futuretools/
│   ├── spiders/
│   │   ├── tool_info_spider.py        # Extracts tool info from tool pages
│   │   └── tool_link_spider.py        # Gathers tool page links from listing pages
│   ├── items.py                        # Defines item fields: ToolLinkItem, ToolInfoItem
│   ├── pipelines.py                    # Saves data and manages DB status transitions
│   ├── middlewares.py                  # Handles 429 Retry-After logic, user-agent rotation
│   ├── settings.py                     # Scrapy configuration (auto-throttle, retry, UAs)
├── ai_tools.db                         # SQLite database to store links and extracted info
├── run_crawler_loop.sh                 # Bash script to run crawler in a loop with control
├── check_new_links.py                 # Checks if any URLs remain with status='NEW'
├── change_status.py                   # Resets 'PROCESSING'/'SCRAPED' statuses to 'NEW'
```

---

## 🚀 Features

### 🕷 Web Crawlers (Scrapy)

* **`tool_link_spider`**:

  * Crawls paginated tool listings from FutureTools.io
  * Extracts individual tool URLs and stores them in SQLite (`tool_links` table)
  * Sets initial status as `'NEW'`

* **`tool_info_spider`**:

  * Loads URLs with `status = 'NEW'` from the database
  * Extracts name, image URL, upvotes, website link, pricing model, description, and tags
  * Marks successful entries as `'DONE'` or stores error code (e.g., `404`, `TIMEOUT`, etc.)

### 🔁 Auto Throttling & Retry Control

* Scrapy's `AUTOTHROTTLE` enabled for adaptive request pacing
* Custom middleware delays retry using `Retry-After` header on 429 responses
* User-agent rotation enabled to reduce bot detection risk

### 🗃 SQLite Storage & Status Management

* `tool_links` table: stores URLs and crawling status
* `tool_info` table: stores extracted tool metadata
* Prevents duplicates with `INSERT OR IGNORE`
* Status is updated throughout pipeline and error handler

### 🔁 Automated Execution Scripts

* `run_crawler_loop.sh`:

  * Runs the `tool_info_spider` in a loop with log rotation
  * Cleans up logs older than 30 minutes
  * Stops automatically when no `'NEW'` links remain

* `check_new_links.py`: returns exit code based on whether new links remain

* `change_status.py`: resets `'PROCESSING'` and `'SCRAPED'` entries to `'NEW'`

---

## 🛠 Installation

1. Clone the repo:

```bash
git clone https://github.com/your-username/futuretools-scraper.git
cd futuretools-scraper
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Scrapy:

```bash
pip install scrapy
```

---

## ⚙ Usage

### 1. Gather Tool URLs

```bash
scrapy crawl tool_link_spider
```

### 2. Run Continuous Info Extraction Loop

```bash
chmod +x run_crawler_loop.sh
./run_crawler_loop.sh
```

### 3. Manually Reset Status if Needed

```bash
python change_status.py
```

---

## 🗃 Database Schema

### `tool_links`

| Field       | Type    | Description                                |
| ----------- | ------- | ------------------------------------------ |
| id          | INTEGER | Primary key                                |
| url         | TEXT    | Unique tool page URL                       |
| status      | TEXT    | `NEW`, `PROCESSING`, `DONE`, or error code |
| created\_at | TEXT    | Timestamp of discovery                     |

### `tool_info`

| Field          | Type    | Description                  |
| -------------- | ------- | ---------------------------- |
| id             | INTEGER | Primary key                  |
| url            | TEXT    | Foreign key from tool\_links |
| name           | TEXT    | Tool name                    |
| image\_url     | TEXT    | Logo or screenshot           |
| upvote\_count  | TEXT    | Displayed upvotes            |
| website\_link  | TEXT    | External site URL            |
| description    | TEXT    | Description text             |
| pricing\_model | TEXT    | Free, Freemium, etc.         |
| tags           | TEXT    | Comma-separated list of tags |

---

## 🧼 Pipeline Logic

* **ToolLinkPipeline**:

  * Saves new links and sets initial `status = 'NEW'`
* **ToolInfoPipeline**:

  * Saves parsed tool metadata
  * Updates original link status to `'DONE'`
  * Skips reprocessing of duplicates

---

## ⚙ Configuration (in `settings.py`)

* `RETRY_ENABLED`, `RETRY_TIMES = 5`
* Custom retry for HTTP 429 + `Retry-After` header logic
* Auto-throttling: enabled with target concurrency = 5
* User-agent rotation enabled with random selection per request

---

## 📄 Example SQLite Query

To list all successfully scraped tools:

```sql
SELECT name, website_link, upvote_count FROM tool_info ORDER BY id DESC LIMIT 10;
```

To find failed fetches:

```sql
SELECT url, status FROM tool_links WHERE status NOT IN ('NEW', 'PROCESSING', 'DONE');
```

---

## 🧪 Testing & Monitoring

* Use `scrapy crawl tool_info_spider --loglevel=INFO`
* Tail logs from `./logs/` or redirect them to debug

---

**Disclaimer**: This project is intended for research, personal enrichment, and educational use.