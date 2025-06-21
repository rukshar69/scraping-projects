import sqlite3

def reset_tool_statuses(db_path="ai_tools.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Update rows where status is 'PROCESSING' or 'SCRAPED' (case-insensitive) to 'NEW'
        cursor.execute("""
            UPDATE tool_links
            SET status = 'NEW'
            WHERE UPPER(status) IN ('PROCESSING', 'SCRAPED')
        """)

        conn.commit()
        print(f"Updated {cursor.rowcount} rows to status 'NEW'.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    reset_tool_statuses()
