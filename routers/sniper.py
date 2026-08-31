from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.sniper import find_snipable_listings

router = APIRouter(prefix="/sniper", tags=["sniper"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/results/{identity_id}")
def get_sniper_results(identity_id: int, db: Session = Depends(get_db)):
    return find_snipable_listings(db, identity_id)
