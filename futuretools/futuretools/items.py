
import scrapy

class ToolLinkItem(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    created_at = scrapy.Field()

class ToolInfoItem(scrapy.Item):
    name = scrapy.Field()
    image_url = scrapy.Field()
    upvote_count = scrapy.Field()
    website_link = scrapy.Field()
    description = scrapy.Field()
    pricing_model = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()  # To trace back the record
