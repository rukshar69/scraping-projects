import re
from scrapy.exceptions import DropItem
from datetime import datetime
import sqlite3

class CleaningPipeline:
    """
    Pipeline to clean and validate scraped data.
    """
    salary_pattern = re.compile(r'([\d,]+)(?:\s*-\s*([\d,]+))?')

    def process_item(self, item, spider):
        #  Add timestamp
        item['scraped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
    
class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("careerjet_jobs.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company TEXT,
                job_link TEXT UNIQUE,
                location TEXT,
                salary TEXT,
                page INTEGER,
                scraped_at DATETIME,
                crawl_status TEXT DEFAULT 'NEW'
            )
        ''')
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT OR IGNORE INTO jobs (
                title, company, job_link, location, salary, page, scraped_at, crawl_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('title'),
            item.get('company'),
            item.get('job_link'),
            item.get('location'),
            item.get('salary'),
            item.get('page'),
            item.get('scraped_at'),
            'NEW'
        ))
        return item
    
class JobDescriptionPipeline:
    def open_spider(self, spider):
        if spider.name != 'careerjet_description':
            return
        self.connection = sqlite3.connect("careerjet_jobs.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_description (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_link TEXT UNIQUE,
                job_description TEXT,
                status TEXT DEFAULT 'NEW'
            )
        ''')
        self.connection.commit()

    def close_spider(self, spider):
        if spider.name != 'careerjet_description':
            return
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        if spider.name != 'careerjet_description':
            return item
        
        self.cursor.execute('''
            INSERT OR REPLACE INTO job_description (job_link, job_description, status)
            VALUES (?, ?, 'NEW')
        ''', (
            item.get('job_link'),
            item.get('job_description'),
        ))
        self.cursor.execute('''
            UPDATE jobs
            SET crawl_status = 'DONE'
            WHERE job_link = ?
        ''', (item.get('job_link'),))
        self.connection.commit()
        return item
