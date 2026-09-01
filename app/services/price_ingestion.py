from sqlalchemy.orm import Session

from app.models.listings import Listing
from app.models.card import Card
from app.services.price_history import record_price_history
from app.scrapers.ebay_au import fetch_ebay_au_prices


def ingest_prices_for_card(db: Session, card: Card) -> None:
    """
    Fetch prices for a card using EBay Australia and insert listings + price history.
    """

    # Resolve set name from identity → set → canonical_name
    try:
        set_name = card.identity.set.canonical_name
    except Exception:
        print(f"[SKIP] Card {card.name} has no linked set")
        return

    # Fetch prices from eBay AU
    prices = fetch_ebay_au_prices(card.name, set_name)

    if not prices:
        print(f"[SKIP] No EBay AU prices for {card.name} ({set_name})")
        return

    # Insert listings + price history
    for raw in prices:
        listing = Listing(
            identity_id=card.identity_id,
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
            source="ebay_au",
        )

    db.commit()
    print(f"[OK] Inserted {len(prices)} EBay AU prices for {card.name}")
