import random
import asyncio
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

async def async_sleep(delay: float):
    await asyncio.sleep(delay)

class TooManyRequestsRetryMiddleware(RetryMiddleware):
    """
    Custom Scrapy middleware to handle HTTP 429 (Too Many Requests) responses.

    This middleware extends Scrapy's default RetryMiddleware to respect the 
    'Retry-After' HTTP header. When a 429 response is received, it delays the 
    retry by the amount of time specified in the header, or falls back to a default
    delay if the header is missing or invalid.

    This helps prevent aggressive retrying and respects server-side rate limits.
    """

    DEFAULT_DELAY = 60   # fallback delay in seconds
    MAX_DELAY = 600      # cap delay at 10 minutes

    async def process_response(self, request, response, spider):
        """
        Processes each response to determine if it should be retried.

        If a response has HTTP status 429, the middleware looks for the
        'Retry-After' header and delays the retry accordingly (asynchronously).
        Falls back to a default delay if the header is absent or invalid.

        All other response statuses are passed to the base RetryMiddleware.
        """
        if request.meta.get('dont_retry', False):
            return response

        if response.status == 429 and response.status in self.retry_http_codes:
            header = response.headers.get('Retry-After')
            try:
                retry_after = int(header)
                delay = min(retry_after, self.MAX_DELAY)
            except (TypeError, ValueError):
                delay = self.DEFAULT_DELAY

            spider.logger.info(f"429 received for {request.url}, delaying retry by {delay}s")
            await async_sleep(delay)
            return self._retry(request, response_status_message(response.status), spider) or response

        return super().process_response(request, response, spider)


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