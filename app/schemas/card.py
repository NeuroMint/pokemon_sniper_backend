from pydantic import BaseModel

class CardBase(BaseModel):
    name: str
    set: str
    number: str
    rarity: str
    language: str
    variant: str

class CardCreate(CardBase):
    pass

class Card(CardBase):
    id: int

    class Config:
        orm_mode = True
