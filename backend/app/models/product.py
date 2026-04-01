from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    category = Column(String)
    source = Column(String)
    external_id = Column(String, index=True)
    price = Column(Float)
    image = Column(String)
    url = Column(String)