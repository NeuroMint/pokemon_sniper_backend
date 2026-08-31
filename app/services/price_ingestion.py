from sqlalchemy.orm import Session

from app.scrapers.tcg_api import fetch_listings_for_card
from app.normalisation.price_normaliser import normalise_listing
from app.models.listings import Listing
from app.models.price_history import PriceHistory
from app.models.card import Card  
from app.services.price_history import record_price_history


def ingest_all_prices(db: Session) -> None:
    cards = db.query(Card).all()  
    for card in cards:
        ingest_prices_for_card(db, card)  # 


def ingest_prices_for_card(db: Session, card: Card) -> None:  
    raw_listings = fetch_listings_for_card(card.id)  

    for raw in raw_listings:
        normalized = normalise_listing(raw)

        listing = Listing(
            identity_id=card.id,  
            price=normalized["price"],
            currency=normalized["currency"],
            condition=normalized["condition"],
            seller=normalized["seller"],
            source_listing_id=normalized["source_listing_id"],
        )
        db.add(listing)

        record_price_history(
            db,
            card_id=card.id,
            price=normalized["price"],
            source="tcgplayer"
        )

    db.commit()
