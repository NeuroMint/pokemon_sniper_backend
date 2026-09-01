from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)

    # Canonical identity link
    identity_id = Column(Integer, ForeignKey("card_identities.id"), nullable=False)
    identity = relationship("CardIdentity", back_populates="cards")

    # Basic fields
    name = Column(String, nullable=False)
    card_number = Column(String, nullable=False)

    # Canonical fields
    number = Column(String, nullable=True)
    suffix = Column(String, nullable=True)

    # Foreign keys
    set_id = Column(Integer, ForeignKey("sets.id"), nullable=True)
    rarity_id = Column(Integer, ForeignKey("rarities.id"), nullable=True)
    variant_id = Column(Integer, ForeignKey("variants.id"), nullable=True)
    language_id = Column(Integer, ForeignKey("languages.id"), nullable=True)

    # Relationships
    set = relationship("Set")
    rarity_rel = relationship("Rarity")
    variant_rel = relationship("Variant")
    language_rel = relationship("Language")

    # Images
    image_url = Column(String, nullable=True)
    image_small = Column(String, nullable=True)
    image_large = Column(String, nullable=True)

    # Source
    source = Column(String, nullable=False)
