import sqlite3
import logging
import time
from llm_job_description_parser_v2 import extract_job_info
from pyrate_limiter import Limiter, Rate, Duration, BucketFullException
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("job_processing.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize rate limiter: 10 requests per minute
rate = Rate(10, Duration.MINUTE)
limiter = Limiter(rate)

def process_and_save_jobs(
    db_path: str = "../careerjet/careerjet_jobs.db",
    batch_size: int = 40
):
    """
    Process unprocessed job descriptions from the SQLite database,
    extract structured information using an LLM, and save the result
    into the job_components table.

    :param db_path: Path to the SQLite database file.
    :param batch_size: Number of job descriptions to process per call.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure destination table exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_components (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_link TEXT UNIQUE,
        job_responsibilities TEXT,
        job_requirements TEXT,
        company_name TEXT,
        company_address TEXT,
        application_email TEXT,
        benefits TEXT,
        compensation TEXT,
        extracted_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

    # Fetch unprocessed jobs
    cursor.execute("""
        SELECT id, job_link, job_description
        FROM job_description
        WHERE status != 'DONE'
        LIMIT ?
    """, (batch_size,))
    rows = cursor.fetchall()

    for job_id, job_link, description in rows:
        try:
            logger.info(f"[Job {job_id}] Starting processing.")

            # Mark as IN_PROGRESS
            cursor.execute("UPDATE job_description SET status = 'IN_PROGRESS' WHERE id = ?", (job_id,))
            conn.commit()
            logger.info(f"[Job {job_id}] Marked as IN_PROGRESS.")

            # Apply rate limiting with manual backoff
            while True:
                try:
                    limiter.try_acquire(job_link)
                    break  # Exit loop if acquisition is successful
                except BucketFullException:
                    wait_time = 60  # Wait for 60 seconds before retrying
                    logger.warning(f"[Job {job_id}] Rate limit exceeded. Sleeping for {wait_time} seconds.")
                    time.sleep(wait_time)

            # Extract job info with retry logic
            result = extract_job_info(description)
            if isinstance(result, dict) and "error" in result:
                logger.error(f"[Job {job_id}] Extraction error: {result['error']}")
                continue

            # Convert Pydantic model to dict
            result_dict = result.model_dump()

            # Save to job_components table
            cursor.execute("""
                INSERT OR REPLACE INTO job_components (
                    job_link, job_responsibilities, job_requirements,
                    company_name, company_address, application_email,
                    benefits, compensation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job_link,
                result_dict.get("job_responsibilities"),
                result_dict.get("job_requirements"),
                result_dict.get("company_name"),
                result_dict.get("company_address"),
                result_dict.get("application_email"),
                result_dict.get("benefits"),
                result_dict.get("compensation")
            ))

            # Mark as DONE
            cursor.execute("UPDATE job_description SET status = 'DONE' WHERE id = ?", (job_id,))
            conn.commit()

            logger.info(f"[Job {job_id}] ✅ Successfully processed and saved.")

        except Exception as e:
            logger.exception(f"[Job {job_id}] ❌ Unexpected error during processing: {e}")

    conn.close()
    logger.info("✅ Job extraction session complete. Database connection closed.")

# Example usage
if __name__ == "__main__":
    process_and_save_jobs()
