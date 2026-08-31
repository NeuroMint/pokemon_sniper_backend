from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.price_history import PriceHistory
from app.models.listings import Listing

router = APIRouter(prefix="/prices", tags=["prices"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/history/{identity_id}")
def get_price_history(identity_id: int, db: Session = Depends(get_db)):
    return (
        db.query(PriceHistory)
        .filter(PriceHistory.identity_id == identity_id)
        .order_by(PriceHistory.created_at.desc())
        .limit(50)
        .all()
    )


@router.get("/listings/{identity_id}")
def get_listings(identity_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Listing)
        .filter(Listing.identity_id == identity_id)
        .order_by(Listing.created_at.desc())
        .limit(50)
        .all()
    )
