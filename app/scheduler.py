import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
import logging
import importlib
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor

from app.database import SessionLocal
import app.scrapers.tcg_api as tcg_api

logging.basicConfig(level=logging.INFO)

# A thread pool for running blocking scrapers
executor = ThreadPoolExecutor(max_workers=1)

def run_scraper_sync():
    """Runs the blocking scraper synchronously inside a thread."""
    importlib.reload(tcg_api)

    db: Session = SessionLocal()
    try:
        tcg_api.run_tcg_api_scraper(db)
        logging.info("Scheduler tick")
    finally:
        db.close()


async def scraper_loop():
    """Async wrapper that schedules the blocking scraper safely."""
    await asyncio.sleep(10)  # delay first run

    while True:
        # Run the blocking scraper in a thread
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(executor, run_scraper_sync)

        # Sleep async (non-blocking)
        await asyncio.sleep(300)
