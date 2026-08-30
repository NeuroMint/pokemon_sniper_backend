from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Variant(Base):
    __tablename__ = "variants"

    id = Column(Integer, primary_key=True, index=True)
    canonical_name = Column(String, index=True)
    category = Column(String, index=True)  
