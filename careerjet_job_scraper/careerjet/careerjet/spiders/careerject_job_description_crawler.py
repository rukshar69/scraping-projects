import scrapy
import sqlite3
from careerjet.items import JobDescriptionItem

class CareerjetDescriptionSpider(scrapy.Spider):
    name = "careerjet_description"
    allowed_domains = ["careerjet.com.bd"]

    custom_settings = {
        'LOG_FILE': 'careerjet_description.log',
        'ITEM_PIPELINES': {
            'careerjet.pipelines.JobDescriptionPipeline': 300,
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = sqlite3.connect("careerjet_jobs.db")
        self.cursor = self.conn.cursor()
        self.batch_size = 50
        self.batch_count = 0
        self.max_batches = 10  # Stop after 2 batches (for testing)
        self.testing = True
        self.in_progress = 0

    def start_requests(self):
        self.logger.info("Starting with first batch of job links")
        yield from self.get_next_batch()

    def get_next_batch(self):
        if self.testing and self.batch_count >= self.max_batches:
            self.logger.info(f"Reached max_batches={self.max_batches}. Stopping spider.")
            return

        self.cursor.execute("SELECT job_link FROM jobs WHERE crawl_status = 'NEW' LIMIT ?", (self.batch_size,))
        rows = self.cursor.fetchall()

        if not rows:
            self.logger.info("No more job links to process.")
            return

        self.batch_count += 1
        self.logger.info(f"[Batch {self.batch_count}] Fetched {len(rows)} job links.")

        # Mark them IN_PROGRESS
        self.cursor.executemany(
            "UPDATE jobs SET crawl_status = 'IN_PROGRESS' WHERE job_link = ?",
            [(job_link,) for (job_link,) in rows]
        )
        self.conn.commit()

        for (job_link,) in rows:
            self.in_progress += 1
            yield scrapy.Request(
                url=job_link,
                callback=self.parse_job,
                errback=self.handle_error,
                meta={'job_link': job_link}
            )

    def parse_job(self, response):
        job_link = response.meta['job_link']
        description = response.xpath("//section[@class='content']//text()").getall()
        cleaned_description = " ".join(part.strip() for part in description if part.strip())

        self.in_progress -= 1

        if not cleaned_description:
            self.logger.warning(f"No description found at {job_link}")
            self.update_job_status(job_link, "NO_DESCRIPTION_FOUND")
        else:
            yield JobDescriptionItem(
                job_link=job_link,
                job_description=cleaned_description
            )

        if self.in_progress == 0:
            yield from self.get_next_batch()

    def handle_error(self, failure):
        job_link = failure.request.meta.get('job_link')
        self.logger.error(f"Failed to process {job_link}: {failure.value}")
        self.update_job_status(job_link, f"ERROR: {str(failure.value)}")
        self.in_progress -= 1

        if self.in_progress == 0:
            yield from self.get_next_batch()

    def update_job_status(self, job_link, status):
        self.cursor.execute(
            "UPDATE jobs SET crawl_status = ? WHERE job_link = ?",
            (status, job_link)
        )
        self.conn.commit()

    def closed(self, reason):
        self.conn.commit()
        self.conn.close()
        self.logger.info(f"Spider closed: {reason}")
