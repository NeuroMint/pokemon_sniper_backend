from pydantic import BaseModel
from datetime import datetime

class CardBase(BaseModel):
    name: str
    set_name: str
    card_number: str
    rarity: str | None = None
    language: str | None = None
    variant: str | None = None
    image_url: str | None = None

class CardCreate(CardBase):
    pass

class CardRead(CardBase):
    id: int
    created_at: datetime | None

    class Config:
        from_attributes = True
