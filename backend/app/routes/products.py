from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.schemas.product import ProductResponse
from app.services.ingestion import ingest_products, sync_real_time_data

router = APIRouter()


# 🔌 DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


# 🔄 REFRESH DATA (REAL-TIME 🔥)
@router.post("/refresh")
async def refresh(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Perform a full real-time sync from actual websites
    result = await sync_real_time_data(db, background_tasks=background_tasks)
    return result


from typing import Optional

# 🔥 GET PRODUCTS WITH FILTER + PAGINATION
@router.get("/products", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db),

    category: Optional[str] = None,
    source: Optional[str] = None,
    brand: Optional[str] = None,

    min_price: Optional[float] = None,
    max_price: Optional[float] = None,

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


from sqlalchemy import func

# 📊 AGGREGATE ANALYTICS
@router.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    total = db.query(Product).count()
    if total == 0:
        return {
            "total_products": 0,
            "average_price": 0,
            "by_source": {},
            "by_category": {}
        }

    avg_price = db.query(func.avg(Product.price)).scalar() or 0

    sources = db.query(Product.source, func.count(Product.id)).group_by(Product.source).all()
    by_source = {s[0]: s[1] for s in sources}

    categories = db.query(Product.category, func.avg(Product.price)).group_by(Product.category).all()
    by_category = {c[0]: round(c[1], 2) for c in categories}

    return {
        "total_products": total,
        "average_price": round(avg_price, 2),
        "by_source": by_source,
        "by_category": by_category
    }
from app.models.event import Event

@router.get("/events")
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events