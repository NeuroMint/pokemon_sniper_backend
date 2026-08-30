from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Rarity(Base):
    __tablename__ = "rarities"

    id = Column(Integer, primary_key=True, index=True)
    canonical_name = Column(String, index=True)
    tier = Column(Integer, index=True)  
    is_holo = Column(Integer, default=0)
    is_ultra = Column(Integer, default=0)
    is_secret = Column(Integer, default=0)
