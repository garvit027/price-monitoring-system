from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.ingestion import ingest_products
from app.models.product import Product

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/refresh")
def refresh(db: Session = Depends(get_db)):
    count = ingest_products(db)
    return {"inserted": count}

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()