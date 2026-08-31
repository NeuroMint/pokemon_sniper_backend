from sqlalchemy.orm import Session
from app.models.listings import Listing
from app.models.card import Card
from app.services.price_history import record_price_history


def ingest_prices_for_card(db: Session, card: Card, raw_card_data: dict) -> None:
    prices = raw_card_data.get("tcgplayer", {}).get("prices", {})
    listings = []

    # Extract price variants from PokémonTCG API
    for variant, price_info in prices.items():
        market_price = price_info.get("market")
        if market_price:
            listings.append({
                "price": market_price,
                "currency": "USD",
                "condition": variant,
                "seller": "tcgplayer",
                "source_listing_id": f"{raw_card_data.get('id')}-{variant}"
            })

    # Insert listings + price history
    for raw in listings:
        listing = Listing(
            identity_id=card.id,
            price=raw["price"],
            currency=raw["currency"],
            condition=raw["condition"],
            seller=raw["seller"],
            source_listing_id=raw["source_listing_id"],
        )
        db.add(listing)

        record_price_history(
            db,
            card_id=card.id,
            price=raw["price"],
            source="tcgplayer"
        )

    db.commit()
