from sqlalchemy import Column, Integer, String, Float, ForeignKey
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
    alert_price = Column(Float, nullable=True, index=True)
    alert_user_email = Column(String, nullable=True)
    collection_id = Column(Integer, ForeignKey("collections.id", ondelete="SET NULL"), nullable=True)

    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")