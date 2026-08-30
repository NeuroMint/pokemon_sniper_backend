from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.card import Card
from app.schemas.card import CardCreate, CardRead

router = APIRouter(
    prefix="/cards",
    tags=["cards"]
)

@router.post("/", response_model=CardRead)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    db_card = Card(**card.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@router.get("/", response_model=list[CardRead])
def get_cards(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Card).offset(skip).limit(limit).all()
