import scrapy
from datetime import datetime
from futuretools.items import ToolLinkItem

class ToolsSpider(scrapy.Spider):
    name = "tool_link_spider"
    allowed_domains = ["futuretools.io"]
    start_urls = [f"https://www.futuretools.io/?b34cbd71_page={i}" for i in range(3, 36)]

    def parse(self, response):
        self.logger.info(f"Parsing page: {response.url}")
        tool_cards = response.xpath('//div[contains(@class, "tool tool-home")]')
        self.logger.info(f"Found {len(tool_cards)} tool cards on the page.")

        for index, card in enumerate(tool_cards, start=1):
            href = card.xpath('.//a/@href').get()
            if href:
                full_url = response.urljoin(href)
                item = ToolLinkItem()
                item['url'] = full_url
                item['status'] = 'NEW'
                item['created_at'] = datetime.now().isoformat()
                self.logger.debug(f"[{index}] Extracted tool URL: {full_url}")
                yield item
            else:
                self.logger.warning(f"[{index}] Tool card has no href: {card.get()}")
