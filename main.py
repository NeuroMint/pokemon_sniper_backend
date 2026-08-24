from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Card, Listing  
from schemas import CardCreate
from schemas import ListingCreate 

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Pokemon Sniper Backend is now live!"}

@app.get("/listings")
def get_listings(db: Session = Depends(get_db)):
    listings = db.query(Listing).all()
    return listings

@app.get("/cards")
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
