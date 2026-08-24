from sqlalchemy import Column, Integer, String, Float, TIMESTAMP  # ← added Float here
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    condition = Column(String)
    seller_name = Column(String)
    seller_feedback_score = Column(Integer)
    seller_positive_percent = Column(Float)
    shipping_cost = Column(Float)
    location = Column(String)
    photos = Column(String)

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    set_name = Column(String, nullable=False)
    card_number = Column(String, nullable=False)
    rarity = Column(String)
    language = Column(String, default="EN")
    variant = Column(String)
    created_at = Column(TIMESTAMP)

from database import engine
Base.metadata.create_all(bind=engine)