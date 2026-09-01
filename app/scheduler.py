import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
import logging
import schedule
import importlib
from sqlalchemy.orm import Session

from app.database import SessionLocal
import app.scrapers.tcg_api as tcg_api

logging.basicConfig(level=logging.INFO)

async def scraper_loop():
    # ⭐ Delay first run to avoid double-scrape on startup
    await asyncio.sleep(10)

    while True:
        importlib.reload(tcg_api)

        db: Session = SessionLocal()
        try:
            tcg_api.run_tcg_api_scraper(db)
            logging.info("Scheduler tick")
        finally:
            db.close()

        await asyncio.sleep(300)


def run_price_ingestion():
    db = SessionLocal()
    try:
        logging.info("Price ingestion stub running...")
    finally:
        db.close()

schedule.every(5).minutes.do(run_price_ingestion)
