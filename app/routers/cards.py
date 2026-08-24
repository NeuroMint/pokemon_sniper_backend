from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.card import Card
from app.schemas.card import CardCreate, Card

router = APIRouter()

@router.post("/cards", response_model=Card)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    db_card = Card(**card.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@router.get("/cards", response_model=list[Card])
def get_cards(db: Session = Depends(get_db)):
    return db.query(Card).all()
