
import scrapy

class ToolItem(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    created_at = scrapy.Field()

