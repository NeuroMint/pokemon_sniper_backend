from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CardIdentity(Base):
    __tablename__ = "card_identities"

    id = Column(Integer, primary_key=True, index=True)

    # Canonical identity fields
    name = Column(String, nullable=False)
    canonical_name = Column(String, nullable=False)

    # Foreign keys to canonical tables
    set_id = Column(Integer, ForeignKey("sets.id"), nullable=True)
    rarity_id = Column(Integer, ForeignKey("rarities.id"), nullable=True)
    variant_id = Column(Integer, ForeignKey("variants.id"), nullable=True)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=True)

    # Card numbering
    number = Column(String, nullable=True)
    suffix = Column(String, nullable=True)
    language = Column(String, nullable=True)


    # Relationship to Card
    cards = relationship("Card", back_populates="identity")
