from datetime import datetime
from sqlalchemy.orm import Session
from app.models.price_history import PriceHistory

def record_price_history(db: Session, card_id: int, price: float, source: str) -> None:
    entry = PriceHistory(
        card_id=card_id,
        price=price,
        source=source,
        created_at=datetime.utcnow(),
    )
    db.add(entry)
    db.commit()
