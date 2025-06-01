import scrapy
from careerjet.items import CareerjetItem
from datetime import datetime

class CareerjetCrawlerSpider(scrapy.Spider):
    name = "careerjet_crawler"
    allowed_domains = ["careerjet.com.bd"]

    def start_requests(self):
        """Generate requests for all pages"""
        base_url = "https://www.careerjet.com.bd/jobs?s=&l=Bangladesh"
        
        # First page (no page parameter needed)
        yield scrapy.Request(
            url=base_url,
            callback=self.parse,
            meta={'page': 1}
        )
        
        # Pages 2-100
        for page in range(2, 101):
            url = f"{base_url}&p={page}"
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={'page': page}
            )

    def parse(self, response):
        """Parse job listings from each page"""
        current_page = response.meta.get('page', 1)
        self.logger.info(f"Parsing page {current_page}: {response.url}")
        
        # Check if page has jobs
        jobs = response.xpath("//ul[@class='jobs']//li/article")
        
        if not jobs:
            self.logger.warning(f"No jobs found on page {current_page}")
            return
        
        for job in jobs:
            # Raw extraction only
            title = job.xpath(".//header/h2/a/text()").get()
            company = job.xpath(".//p[@class='company']//text()").getall() or None
            job_link = job.xpath(".//header/h2/a/@href").get()
            location = job.xpath(".//ul[@class='location']//text()").getall() or None
            salary = job.xpath(".//ul[@class='salary']//text()").getall() or None

            item = CareerjetItem(
                title=title,
                company=company,
                job_link=job_link,
                location=location,
                salary=salary,
                page=current_page,
            )
            yield item

        # Log completion of page
        self.logger.info(f"Completed parsing page {current_page}")
