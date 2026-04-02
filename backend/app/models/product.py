from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String, index=True)
    category = Column(String, index=True)
    source = Column(String, index=True)
    external_id = Column(String, index=True)
    price = Column(Float, index=True)
    image = Column(String)
    url = Column(String)

    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")