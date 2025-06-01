import re
from scrapy.exceptions import DropItem
from datetime import datetime

class CleaningPipeline:
    """
    Pipeline to clean and validate scraped data.
    """
    salary_pattern = re.compile(r'([\d,]+)(?:\s*-\s*([\d,]+))?')

    def process_item(self, item, spider):
        #  Add timestamp
        item['scraped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        # Title must exist
        if not item.get('title'):
            spider.logger.warning('Missing title for item: %r', item)
            raise DropItem('Missing title')
        item['title'] = item['title'].strip()

        # Company can be empty, but log if missing
        if not item.get('company'):
            spider.logger.info('Company missing for "%s"', item['title'])
        else:
            company = " ".join([part.strip() for part in item['company'] if part.strip()])
            item['company'] = company if company else None

        # Normalize salary
        raw = item.get('salary') or ''
        raw = "".join([part.strip() for part in raw if part.strip()])
        m = self.salary_pattern.search(raw)
        if m:
            low = m.group(1).replace(',', '')
            high = m.group(2).replace(',', '') if m.group(2) else None
            item['salary'] = f"{low}-{high}" if high else low
        else:
            item['salary'] = None

        # Normalize job_link to absolute
        # Normalize job_link to absolute
        link = item.get('job_link')
        if link and not link.startswith('http'):
            base_url = "https://www.careerjet.com.bd"
            item['job_link'] = base_url + link
        elif not link:
            item['job_link'] = None
        
        # Normalize location
        location = item.get('location') or []
        location_str = " ".join([part.strip() for part in location if part.strip()])
        item['location'] = location_str if location_str else None
        
        return item
    
