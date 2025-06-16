from scrapy import signals
import random

class RotateUserAgentMiddleware:
    """
    Rotate user-agent for each request using a predefined list.
    """
    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('USER_AGENT_LIST', []))

    def process_request(self, request, spider):
        if self.user_agents:
            request.headers.setdefault('User-Agent', random.choice(self.user_agents))