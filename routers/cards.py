from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.card import Card
from app.schemas.card import CardCreate, Card as CardSchema

router = APIRouter(
    prefix="/cards",
    tags=["cards"]
)

@router.post("/", response_model=CardSchema)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    db_card = Card(**card.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@router.get("/", response_model=list[CardSchema])
def get_cards(db: Session = Depends(get_db)):
    return db.query(Card).all()
