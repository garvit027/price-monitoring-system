from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.models.event import Event
from app.models.user import User
from app.routes.auth import get_current_user
from app.schemas.product import ProductResponse
from app.services.ingestion import ingest_products, sync_real_time_data
from app.services.scraper import fetch_page_content
from app.services.parsers import get_parser
from app.services.normalizer import clean_product_data, is_valid_product
from app.services.retry import retry
from typing import Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

def get_currency_symbol(source: str) -> str:
    if source in ["Flipkart", "Myntra", "Amazon India"]:
        return "₹"
    return "$"

router = APIRouter()


# 🔌 DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





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
    limit: int = 100
):
    query = db.query(Product)

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

    return query.order_by(Product.id.desc()).offset(skip).limit(limit).all()


# 🔍 GET SINGLE PRODUCT
@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# 📈 PRICE HISTORY
@router.get("/products/{product_id}/history")
def get_price_history(product_id: int, db: Session = Depends(get_db)):
    history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id
    ).order_by(PriceHistory.timestamp.asc()).all()

    if not history:
        return []

    return history


# 🌐 TRACK ANY URL (new endpoint!)
class TrackUrlRequest(BaseModel):
    url: str


@router.post("/track")
async def track_url(payload: TrackUrlRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Accept any product URL, scrape it, and add it to tracking.
    Works with Amazon, Flipkart, Grailed, Fashionphile, 1stdibs, and any other site.
    """
    url = payload.url.strip()

    # Check if already tracked
    existing = db.query(Product).filter(Product.url == url).first()
    if existing:
        return {"status": "already_tracked", "product_id": existing.id, "product": {
            "id": existing.id, "name": existing.name, "price": existing.price,
            "source": existing.source, "image": existing.image
        }}

    # Fetch and parse
    html = await retry(fetch_page_content, url)
    if not html:
        raise HTTPException(status_code=422, detail="Could not fetch the URL. The site may be blocking scrapers.")

    parser, source_name = get_parser(url)
    parsed_data = parser(html)

    if not parsed_data.get("price"):
        raise HTTPException(status_code=422, detail="Could not extract price from this URL. The page structure may not be supported yet.")

    product_data = clean_product_data(parsed_data, source_name, url)

    if not is_valid_product(product_data):
        raise HTTPException(status_code=422, detail="Scraped data is invalid, looks like a bot-check page or missing information. Please try again.")

    product = Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)

    # Seed initial price history
    history = PriceHistory(product_id=product.id, price=product.price)
    db.add(history)
    db.commit()

    logger.info(f"✅ Tracked new product: {product.name} from {source_name} @ {get_currency_symbol(source_name)}{product.price}")

    return {"status": "tracking_started", "product_id": product.id, "product": {
        "id": product.id, "name": product.name, "price": product.price,
        "source": product.source, "image": product.image
    }}


# 📊 AGGREGATE ANALYTICS (with purchase count per site)
@router.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    total = db.query(Product).count()
    if total == 0:
        return {
            "total_products": 0,
            "average_price": 0,
            "by_source": {},
            "by_category": {},
            "purchases_by_source": {},
            "active_anomalies": 0,
        }

    avg_price = db.query(func.avg(Product.price)).scalar() or 0

    sources = db.query(Product.source, func.count(Product.id)).group_by(Product.source).all()
    by_source = {s[0]: s[1] for s in sources}

    categories = db.query(Product.category, func.avg(Product.price)).group_by(Product.category).all()
    by_category = {c[0]: round(c[1], 2) for c in categories}

    # Purchase count = number of price_history records per source (proxy for engagement/checks)
    purchases_by_source_raw = (
        db.query(Product.source, func.count(PriceHistory.id))
        .join(PriceHistory, PriceHistory.product_id == Product.id)
        .group_by(Product.source)
        .all()
    )
    purchases_by_source = {row[0]: row[1] for row in purchases_by_source_raw}

    # Count anomalies
    anomalies_count = db.query(Event).filter(Event.type.in_(["PRICE_CHANGE", "PRICE_ALERT"])).count()

    return {
        "total_products": total,
        "average_price": round(avg_price, 2),
        "by_source": by_source,
        "by_category": by_category,
        "purchases_by_source": purchases_by_source,
        "active_anomalies": anomalies_count,
    }


# 🔔 EVENTS
@router.get("/events")
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).order_by(Event.timestamp.desc()).limit(50).all()
    return events


# 🚨 CONFIGURE PRICE ALERT
class SetAlertRequest(BaseModel):
    alert_price: Optional[float] = None


@router.post("/products/{product_id}/alert")
def set_product_alert(product_id: int, payload: SetAlertRequest, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.alert_price = payload.alert_price
    db.commit()
    db.refresh(product)

    # Log event
    if product.alert_price is not None:
        message = f"Set price alert on {product.name} at {get_currency_symbol(product.source)}{product.alert_price}"
    else:
        message = f"Removed price alert from {product.name}"
    event = Event(type="ALERT_CONFIG", message=message, product_id=product.id)
    db.add(event)
    db.commit()

    return {"status": "alert_price_updated", "alert_price": product.alert_price}


# 🗑️ DELETE PRODUCT
@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"status": "deleted", "product_id": product_id}