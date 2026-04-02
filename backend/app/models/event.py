from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    type = Column(String)  # "PRICE_CHANGE"
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)