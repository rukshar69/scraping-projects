import sqlite3

def has_new_links(db_path="ai_tools.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tool_links WHERE status = 'NEW'")
        count = cursor.fetchone()[0]
        conn.close()

        if count > 0:
            print(f"{count} NEW link(s) found.")
            exit(0)  # Exit code 0 means "continue"
        else:
            print("No NEW links found.")
            exit(1)  # Exit code 1 means "stop"
    except Exception as e:
        print(f"Error checking for NEW links: {e}")
        exit(2)  # Exit code 2 means "error"
        
if __name__ == "__main__":
    has_new_links()
