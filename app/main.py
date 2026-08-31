from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
import asyncio
import threading
from app.database import get_db, Base, engine
from app.models.card import Card
from app.models.listings import Listing
from app.models.price_history import PriceHistory
from app.models.alerts import Alert
from app.models.ingestion_logs import IngestionLog
from app.schemas.card import CardCreate, CardRead
from app.schemas.listing import ListingCreate
from app.scheduler import scraper_loop
from routers import cards, prices, sniper, alerts
from routers.ingestion_logs import router as ingestion_logs_router


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(cards.router)
app.include_router(ingestion_logs_router)
app.include_router(prices.router)
app.include_router(sniper.router)
app.include_router(alerts.router)

@app.on_event("startup")
def start_scheduler():
    thread = threading.Thread(target=asyncio.run, args=(scraper_loop(),))
    thread.daemon = True
    thread.start()
@app.get("/")
def read_root():
    return {"message": "Pokemon Sniper Backend is now live!"}


@app.get("/listings")
def get_listings(db: Session = Depends(get_db)):
    return db.query(Listing).all()


@app.get("/cards", response_model=List[CardRead])
def get_cards(db: Session = Depends(get_db)):
    return db.query(Card).all()


@app.post("/listings")
def create_listing(listing: ListingCreate, db: Session = Depends(get_db)):
    new_listing = Listing(
        title=listing.title,
        price=listing.price,
        condition=listing.condition,
        seller_name=listing.seller_name,
        seller_feedback_score=listing.seller_feedback_score,
        seller_positive_percent=listing.seller_positive_percent,
        shipping_cost=listing.shipping_cost,
        location=listing.location,
        photos=listing.photos
    )
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    return new_listing


@app.post("/cards")
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    new_card = Card(
        name=card.name,
        set_name=card.set_name,
        card_number=card.card_number,
        rarity=card.rarity,
        language=card.language,
        variant=card.variant
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card
