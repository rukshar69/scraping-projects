import sqlite3

conn = sqlite3.connect("careerjet_jobs.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(job_link) FROM jobs WHERE crawl_status = 'NEW'")
rows = cursor.fetchall()
for row in rows:
    print(row)