import sqlite3

class ToolInfoPipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect("ai_tools.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tool_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                name TEXT,
                image_url TEXT,
                upvote_count TEXT,
                website_link TEXT,
                description TEXT,
                pricing_model TEXT,
                tags TEXT
            )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT OR IGNORE INTO tool_info (
                url, name, image_url, upvote_count, website_link,
                description, pricing_model, tags
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get('url'),
            item.get('name'),
            item.get('image_url'),
            item.get('upvote_count'),
            item.get('website_link'),
            item.get('description'),
            item.get('pricing_model'),
            ", ".join(item.get('tags', []))
        ))
        self.cursor.execute("UPDATE tool_links SET status = 'DONE' WHERE url = ?", (item['url'],))
        return item

class ToolLinkPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("ai_tools.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tool_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                status TEXT DEFAULT 'NEW',
                created_at TEXT
            )
        """)
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT OR IGNORE INTO tool_links (url, status, created_at)
            VALUES (?, ?, ?)
        """, (item['url'], item['status'], item['created_at']))
        return item
