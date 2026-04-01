from pydantic import BaseModel

class ProductResponse(BaseModel):
    id: int
    name: str
    brand: str
    category: str
    source: str
    external_id: str
    price: float
    image: str | None = None
    url: str | None = None

    class Config:
        from_attributes = True