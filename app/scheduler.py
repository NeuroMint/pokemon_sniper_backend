import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
import logging
import schedule
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.scrapers.tcg_api import run_tcg_api_scraper

logging.basicConfig(level=logging.INFO)


async def scraper_loop():
    while True:
        db: Session = SessionLocal()
        try:
            run_tcg_api_scraper(db)
            logging.info("Scheduler tick")
        finally:
            db.close()

        await asyncio.sleep(300)  # run every 5 minutes


def run_price_ingestion():
    db = SessionLocal()
    try:
        logging.info("Price ingestion stub running...")
        # later: call your real price ingestion function here
    finally:
        db.close()


schedule.every(5).minutes.do(run_price_ingestion)
