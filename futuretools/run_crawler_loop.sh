#!/bin/bash

# --- CONFIGURATION ---
LIMIT=40                               # Number of tool URLs to process per run
CRAWL_NAME="tool_info_spider"          # Scrapy spider name
LOG_DIR="./logs"                       # Directory for storing logs
DELAY=30                               # Delay in seconds between runs
CHECK_SCRIPT="check_new_links.py"      # Python script to check DB
LOG_RETENTION_MINUTES=15               # Delete logs older than this

# --- SETUP ---
mkdir -p "$LOG_DIR"

echo "==> Starting continuous crawl loop..."

# --- MAIN LOOP ---
while true; do
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    LOG_FILE="$LOG_DIR/crawl_$TIMESTAMP.log"

    echo ""
    echo "[$(date)] Running spider (limit=$LIMIT)..."
    scrapy crawl "$CRAWL_NAME" -a limit="$LIMIT" > "$LOG_FILE" 2>&1

    echo "[$(date)] Crawl complete. Checking for remaining NEW links..."
    python3 "$CHECK_SCRIPT"
    RESULT=$?

    if [ $RESULT -eq 1 ]; then
        echo "[$(date)] No NEW links remaining. Exiting loop."
        break
    elif [ $RESULT -eq 2 ]; then
        echo "[$(date)] Error while checking DB. Exiting loop with error."
        break
    fi

    echo "[$(date)] Cleaning up logs older than $LOG_RETENTION_MINUTES minutes..."
    find "$LOG_DIR" -name "crawl_*.log" -mmin +$LOG_RETENTION_MINUTES -delete

    echo "[$(date)] Sleeping $DELAY seconds before next crawl..."
    sleep $DELAY
done

echo "==> Crawler loop exited."
