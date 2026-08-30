import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.scrapers.tcg_api import run_tcg_api_scraper
import logging

logging.basicConfig(level=logging.INFO)

async def scraper_loop():
    while True:
        db: Session = SessionLocal()
        try:
            run_tcg_api_scraper(db)
            logging.info("Scheduler tick")
        finally:
            db.close()

        await asyncio.sleep(10)  # run every hour
