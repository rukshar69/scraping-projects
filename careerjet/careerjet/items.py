# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CareerjetItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    job_link = scrapy.Field()
    location = scrapy.Field()
    salary = scrapy.Field()
    page = scrapy.Field()  # Track which page the job was found on
    scraped_at = scrapy.Field()  # Timestamp when scraped