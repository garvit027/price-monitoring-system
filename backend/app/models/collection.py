from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    user_email = Column(String, index=True, nullable=False)
