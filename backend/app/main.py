from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.routes import products

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Price Monitoring System")

app.include_router(products.router)