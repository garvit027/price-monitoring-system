from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.schemas.product import ProductResponse
from app.services.ingestion import ingest_products

router = APIRouter()


# 🔌 DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


# 🔄 REFRESH DATA (UPDATED)
@router.post("/refresh")
def refresh(db: Session = Depends(get_db)):
    result = ingest_products(db)
    return result


# 🔥 GET PRODUCTS WITH FILTER + PAGINATION
@router.get("/products", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db),

    category: str | None = None,
    source: str | None = None,
    brand: str | None = None,

    min_price: float | None = None,
    max_price: float | None = None,

    skip: int = 0,
    limit: int = 20
):
    query = db.query(Product)

    # 🔍 Filters
    if category:
        query = query.filter(Product.category == category)

    if source:
        query = query.filter(Product.source == source)

    if brand:
        query = query.filter(Product.brand == brand)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # 📦 Pagination
    products = query.offset(skip).limit(limit).all()

    return products


# 🔍 GET SINGLE PRODUCT
@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# 📈 PRICE HISTORY ENDPOINT (NEW 🔥)
@router.get("/products/{product_id}/history")
def get_price_history(product_id: int, db: Session = Depends(get_db)):
    history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id
    ).all()

    if not history:
        return {"message": "No price history found"}

    return history


# 📊 BASIC ANALYTICS
@router.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    total = len(products)

    if total == 0:
        return {
            "total_products": 0,
            "average_price": 0
        }

    avg_price = sum(p.price for p in products) / total

    return {
        "total_products": total,
        "average_price": round(avg_price, 2)
    }
from app.models.event import Event

@router.get("/events")
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events