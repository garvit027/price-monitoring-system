from pydantic import BaseModel

class CollectionBase(BaseModel):
    name: str

class CollectionCreate(CollectionBase):
    pass

class CollectionResponse(CollectionBase):
    id: int
    user_email: str

    class Config:
        from_attributes = True
