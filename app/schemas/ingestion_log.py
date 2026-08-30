from pydantic import BaseModel
from datetime import datetime

class IngestionLogRead(BaseModel):
    id: int
    source: str
    status: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
