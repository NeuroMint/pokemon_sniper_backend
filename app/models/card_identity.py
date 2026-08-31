from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from app.database import SessionLocal


class CardIdentity(Base):
    __tablename__ = "card_identities"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, index=True)
    set_id = Column(Integer, ForeignKey("sets.id"))
    number = Column(Integer, index=True)
    suffix = Column(String, nullable=True)

    variant_id = Column(Integer, ForeignKey("variants.id"), nullable=True)
    rarity_id = Column(Integer, ForeignKey("rarities.id"), nullable=True)

    language = Column(String, default="EN")
