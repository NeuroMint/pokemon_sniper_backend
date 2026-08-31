from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database import Base


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    source = Column(String, nullable=False)
    recorded_at = Column(DateTime, nullable=False)
