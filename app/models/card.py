from sqlalchemy import Column, Integer, String
from app.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    set = Column(String, index=True, nullable=False)
    number = Column(String, index=True, nullable=False)
    rarity = Column(String, nullable=True)
    language = Column(String, nullable=True)
    variant = Column(String, nullable=True)
