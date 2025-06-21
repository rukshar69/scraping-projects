import scrapy
import sqlite3
from ..items import ToolInfoItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError

class FutureToolsSpider(scrapy.Spider):
    name = "tool_info_spider"
    custom_settings = {
        'ITEM_PIPELINES': {'futuretools.pipelines.ToolInfoPipeline': 1},
    }

    def __init__(self, limit=50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limit = int(limit)

    def start_requests(self):
        self.conn = sqlite3.connect("ai_tools.db")
        self.cursor = self.conn.cursor()

        # Fetch NEW links
        self.cursor.execute("SELECT url FROM tool_links WHERE status = 'NEW' LIMIT ?", (self.limit,))
        rows = self.cursor.fetchall()

        self.urls = []
        for row in rows:
            url = row[0]
            # Mark as PROCESSING immediately
            self.cursor.execute("UPDATE tool_links SET status = 'PROCESSING' WHERE url = ?", (url,))
            self.urls.append(url)

        self.conn.commit()
        self.conn.close()  # Avoid leaving open connection

        # Now yield the requests
        for url in self.urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.handle_error,
                meta={'tool_url': url},
            )


    def parse(self, response):
        item = ToolInfoItem()
        item['url'] = response.meta['tool_url']
        item['name'] = response.xpath("//div[@class='tool-main-content']/h1[@class='heading-3']/text()").get()
        item['image_url'] = response.xpath("//div[@class='tool-main-content']//div[@class='cell-2']/a/img/@src").get()
        item['upvote_count'] = response.xpath("//div[@class='tool-main-content']//div[@class='cell-2']/div[contains(@class, 'upvote')]/div[contains(@class, 'upvoted') or contains(@class, 'not-upvoted')]/a/div/text()").get()
        item['website_link'] = response.xpath("//div[@class='tool-main-content']//div[@class='cell-2']/a/@href").get()
        item['description'] = response.xpath(
            "normalize-space(//div[@class='tool-main-content']//div[@class='cell-2']/div[@class='rich-text-block w-richtext'])"
        ).get()
        item['pricing_model'] = response.xpath("//strong[text()='Pricing Model:']/parent::div/following-sibling::div[1]/text()").get()
        item['tags'] = response.xpath("//div[text()='Tags:']/following-sibling::div//a/div/text()").getall()

        yield item

    def handle_error(self, failure):
        url = failure.request.meta['tool_url']

        # Default error label
        error_code = 'ERROR'

        # Determine the error type
        if failure.check(HttpError):
            response = failure.value.response
            error_code = str(response.status)  # e.g., '404' or '500'
        elif failure.check(DNSLookupError):
            error_code = 'DNS_ERROR'
        elif failure.check(TimeoutError) or failure.check(TCPTimedOutError):
            error_code = 'TIMEOUT'
        else:
            error_code = failure.getErrorMessage().split('\n')[0][:50]

        self.logger.warning(f"[{url}] failed due to: {error_code}")

        # Perform isolated DB update (safe)
        try:
            with sqlite3.connect("ai_tools.db") as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE tool_links SET status = ? WHERE url = ?", (error_code, url))
                conn.commit()
        except Exception as e:
            self.logger.error(f"Failed to update status for {url}: {e}")

    def closed(self, reason):
        self.conn.close()
