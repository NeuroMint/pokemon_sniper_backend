from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship




class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    set_name = Column(String, nullable=False)
    card_number = Column(String, nullable=False)
    rarity = Column(String, nullable=True)
    language = Column(String, nullable=False)
    variant = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    source = Column(String, nullable=False)
    identity_id = Column(Integer, ForeignKey("card_identities.id"), nullable=False)
    identity = relationship("CardIdentity", back_populates="cards")

