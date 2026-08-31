from sqlalchemy import Column, Integer, Float, DateTime, func, String
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, index=True)
    listing_id = Column(Integer, index=True)
    discount = Column(Float)
    price = Column(Float)
    avg_price = Column(Float)
    source_listing_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
