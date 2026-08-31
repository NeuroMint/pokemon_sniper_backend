from app.database import SessionLocal
from app.models.card import Card
from app.services.price_ingestion import ingest_prices_for_card

db = SessionLocal()
cards = db.query(Card).all()

for card in cards:
    ingest_prices_for_card(db, card)
