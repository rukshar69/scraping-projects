

BOT_NAME = "careerjet"

SPIDER_MODULES = ["careerjet.spiders"]
NEWSPIDER_MODULE = "careerjet.spiders"

# Logging settings
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_LEVEL = 'INFO'  # Options: CRITICAL, ERROR, WARNING, INFO, DEBUG
LOG_STDOUT = True  # Redirect stdout (print) to log
LOG_FILE = 'careerjet.log'

# Politeness and throttling
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1.2
RANDOMIZE_DOWNLOAD_DELAY = 0.3  # Add randomization to delays
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_TARGET_CONCURRENCY = 2
AUTOTHROTTLE_MAX_DELAY = 10

# Concurrency tuning
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 3
DOWNLOAD_TIMEOUT = 15

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Rotating User Agents
DOWNLOADER_MIDDLEWARES = {
    'careerjet.middlewares.RotateUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
}

# HTTP caching for local development
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600  # 1 hour
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [404, 403, 500, 503]


# Item Pipelines
ITEM_PIPELINES = {
    'careerjet.pipelines.CleaningPipeline': 300,
}

# Feed export
FEEDS = {
    'output/jobs.csv': {
        'format': 'csv',
        'encoding': 'utf8',
        'store_empty': False,
        'overwrite': True,
    },
}

# User agents - Updated with more recent ones
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
]

# Additional settings for better scraping
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}