import sqlite3

class SQLitePipeline:
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
