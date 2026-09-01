from sqlalchemy import Column, Integer, String
from app.database import Base

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    canonical_name = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
