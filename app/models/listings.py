from sqlalchemy import Column, Integer, Float, String
from app.database import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    identity_id = Column(Integer, nullable=False)  # links to Card.id
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    condition = Column(String, nullable=True)
    seller = Column(String, nullable=False)
    source_listing_id = Column(String, nullable=False)
