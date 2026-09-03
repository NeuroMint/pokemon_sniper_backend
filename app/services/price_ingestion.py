from sqlalchemy.orm import Session

from app.models.listings import Listing
from app.models.card import Card
from app.models.set import Set
from app.services.price_history import record_price_history
from app.scrapers.ebay_api import search_ebay_prices




def ingest_prices_for_card(db: Session, card: Card) -> None:
    """
    Fetch prices for a card using EBay Australia and insert listings + price history.
    """

    # --- FIX: Avoid lazy-loading. Fetch Set directly via identity.set_id ---
    identity = card.identity
    if not identity or not identity.set_id:
        print(f"[SKIP] Card {card.name} has no identity.set_id")
        return

    set_obj = db.query(Set).get(identity.set_id)
    if not set_obj:
        print(f"[SKIP] Card {card.name} set_id={identity.set_id} missing Set row")
        return

    set_name = set_obj.canonical_name

    # Fetch prices from eBay AU
    prices = search_ebay_prices(card.name, set_name)

    if not prices:
        print(f"[SKIP] No eBay API prices for {card.name} ({set_name})")
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
