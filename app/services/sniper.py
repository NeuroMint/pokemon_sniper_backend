from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.listings import Listing
from app.models.price_history import PriceHistory
from app.services.alerts import create_alert, alert_exists
from app.services.discord import send_discord_alert


def get_recent_average_price(db: Session, card_id: int, days: int = 7) -> float:
    cutoff = datetime.utcnow() - timedelta(days=days)

    prices = (
        db.query(PriceHistory)
        .filter(
            PriceHistory.card_id == card_id,
            PriceHistory.created_at >= cutoff,
        )
        .all()
    )

    if not prices:
        return None

    return sum(p.price for p in prices) / len(prices)


def find_snipable_listings(db: Session, card_id: int, discount_threshold: float = 0.8):
    avg_price = get_recent_average_price(db, card_id)
    if not avg_price or avg_price <= 0:
        return []

    listings = (
        db.query(Listing)
        .filter(Listing.card_id == card_id)
        .order_by(Listing.created_at.desc())
        .all()
    )

    snipes = []
    for listing in listings:
        if listing.condition not in ["NM", "Near Mint"]:
            continue

        if listing.price <= discount_threshold * avg_price:
            snipe = {
                "listing_id": listing.id,
                "card_id": card_id,
                "price": listing.price,
                "avg_price": avg_price,
                "discount": round(1 - (listing.price / avg_price), 2),
                "source_listing_id": listing.source_listing_id,
            }

            # 🔔 Send alert only once per listing
            if not alert_exists(db, listing.id):
                create_alert(db, snipe)
                send_discord_alert(snipe)

            snipes.append(snipe)

    return snipes
