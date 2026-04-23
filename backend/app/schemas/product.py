from pydantic import BaseModel
from typing import Optional

class ProductResponse(BaseModel):
    id: int
    name: str
    brand: str
    category: str
    source: str
    external_id: str
    price: float
    image: Optional[str] = None
    url: Optional[str] = None

    class Config:
        from_attributes = True