from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, index=True)
    price = Column(Float)
    source = Column(String)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())

