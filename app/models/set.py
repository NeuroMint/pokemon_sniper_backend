from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Set(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, index=True)
    canonical_name = Column(String, index=True)
    series = Column(String, index=True)
    tcg_api_code = Column(String, index=True)
