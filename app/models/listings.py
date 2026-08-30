from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    url = Column(String, nullable=False)
    seller = Column(String)
    condition = Column(String)
    source = Column(String)  # ebay, tcgplayer, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
