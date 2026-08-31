from sqlalchemy.orm import Session
from app.models.alerts import Alert

def create_alert(db: Session, snipe: dict):
    alert = Alert(
        card_id=snipe["card_id"],
        listing_id=snipe["listing_id"],
        discount=snipe["discount"],
        price=snipe["price"],
        avg_price=snipe["avg_price"],
        source_listing_id=snipe["source_listing_id"],
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def alert_exists(db: Session, listing_id: int) -> bool:
    return db.query(Alert).filter(Alert.listing_id == listing_id).first() is not None
