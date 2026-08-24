from pydantic import BaseModel

class CardCreate(BaseModel):
    name: str
    set_name: str
    card_number: str
    rarity: str | None = None
    language: str | None = "EN"
    variant: str | None = None

class ListingCreate(BaseModel):
    title: str
    price: float
    condition: str | None = None
    seller_name: str | None = None
    seller_feedback_score: int | None = None
    seller_positive_percent: float | None = None
    shipping_cost: float | None = None
    location: str | None = None
    photos: str | None = None
