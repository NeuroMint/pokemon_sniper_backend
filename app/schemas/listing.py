from pydantic import BaseModel

class ListingBase(BaseModel):
    title: str
    price: float
    condition: str | None = None
    seller_name: str | None = None
    seller_feedback_score: int | None = None
    seller_positive_percent: float | None = None
    shipping_cost: float | None = None
    location: str | None = None
    photos: str | None = None

class ListingCreate(ListingBase):
    pass

class ListingRead(ListingBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True
