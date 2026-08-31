import asyncio
import logging
import schedule
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.scrapers.tcg_api import run_tcg_api_scraper
from app.services.price_ingestion import ingest_all_prices

logging.basicConfig(level=logging.INFO)


async def scraper_loop():
    while True:
        db: Session = SessionLocal()
        try:
            run_tcg_api_scraper(db)
            ingest_all_prices(db)
            logging.info("Scheduler tick")
        finally:
            db.close()

        await asyncio.sleep(300)  # run every 5 minutes


def run_price_ingestion():
    db = SessionLocal()
    try:
        ingest_all_prices(db)
    finally:
        db.close()


schedule.every(5).minutes.do(run_price_ingestion)
