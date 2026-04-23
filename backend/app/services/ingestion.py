from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.models.event import Event
from app.services.loader import load_products
from app.services.parsers import get_parser
from app.services.normalizer import normalize
from app.services.notification import send_notification
from app.services.retry import retry
from app.services.scraper import fetch_page_content
from app.services.discovery import discover_all
import logging

logger = logging.getLogger(__name__)

async def ingest_products(db: Session, background_tasks=None):
    # (Legacy/Sample file ingestion - keeping for compatibility)
    inserted = 0
    updated = 0

    async for raw_data, filename in load_products():
        parser, source = get_parser(filename)
        if not parser: continue

        parsed = parser(raw_data)
        product_data = normalize(parsed, source, filename)

        existing = db.query(Product).filter(
            Product.external_id == product_data["external_id"],
            Product.source == product_data["source"]
        ).first()

        if not existing:
            product = Product(**product_data)
            db.add(product)
            db.commit()
            db.refresh(product)
            history = PriceHistory(product_id=product.id, price=product.price)
            db.add(history)
            inserted += 1
        else:
            if existing.price != product_data["price"]:
                history = PriceHistory(product_id=existing.id, price=product_data["price"])
                db.add(history)
                message = f"{existing.name} price changed: {existing.price} → {product_data['price']}"
                event = Event(type="PRICE_CHANGE", message=message, product_id=existing.id)
                db.add(event)
                if background_tasks: background_tasks.add_task(send_notification, message)
                existing.price = product_data["price"]
                updated += 1

    db.commit()
    return {"inserted": inserted, "updated": updated}

async def enforce_limit(db: Session, limit: int = 200):
    """
    Ensures the database does not exceed the specified limit of products.
    Removes oldest products first.
    """
    total = db.query(Product).count()
    if total > limit:
        to_delete = total - limit
        logger.info(f"DB size {total} exceeds limit {limit}. Evicting {to_delete} oldest items.")
        
        # Find oldest products by ID
        oldest = db.query(Product).order_by(Product.id.asc()).limit(to_delete).all()
        for p in oldest:
            db.delete(p)
        db.commit()
        return to_delete
    return 0

async def auto_discover_and_grow(db: Session, background_tasks=None):
    """
    Performs discovery of new products and syncs existing ones.
    """
    # 1. Sync Existing
    sync_result = await sync_real_time_data(db, background_tasks)
    
    # 2. Discover New
    discovery_map = await discover_all()
    new_inserted = 0
    
    for source, urls in discovery_map.items():
        for url in urls:
            # Check if exists
            exists = db.query(Product).filter(Product.url == url).first()
            if exists: continue
            
            # Fetch and Parse
            html = await retry(fetch_page_content, url)
            if not html: continue
            
            parser, src_name = get_parser(url)
            if not parser: continue
            
            parsed_data = parser(html)
            if not isinstance(parsed_data, dict) or "price" not in parsed_data: continue
            
            # We need to fill missing fields for new product
            product_data = {
                "name": parsed_data.get("name", "Unknown Product"),
                "brand": parsed_data.get("brand", "Generic"),
                "category": parsed_data.get("category", "General"),
                "source": src_name,
                "external_id": str(parsed_data.get("external_id", hash(url))),
                "price": parsed_data["price"],
                "image": parsed_data.get("image"),
                "url": url
            }
            
            product = Product(**product_data)
            db.add(product)
            db.commit()
            db.refresh(product)
            
            # Seed history
            history = PriceHistory(product_id=product.id, price=product.price)
            db.add(history)
            new_inserted += 1
            
            # Stop if we hit a reasonable batch size to avoid long blocking
            if new_inserted >= 30: break
    
    # 3. Enforce Limit
    evicted = await enforce_limit(db, 200)
    
    return {
        "synced": sync_result["updated"],
        "new_discovered": new_inserted,
        "evicted": evicted,
        "total_errors": sync_result["errors"]
    }

async def sync_real_time_data(db: Session, background_tasks=None):
    products = db.query(Product).filter(Product.url != None).all()
    updated_count = 0
    errors = 0

    for product in products:
        parser, source = get_parser(product.url)
        if not parser: continue

        html = await retry(fetch_page_content, product.url)
        if not html:
            errors += 1
            continue

        parsed_res = parser(html)
        new_price = parsed_res.get("price") if isinstance(parsed_res, dict) else None
        
        if new_price and new_price != product.price:
            history = PriceHistory(product_id=product.id, price=new_price)
            db.add(history)
            message = f"REAL-TIME UPDATE: {product.name} price changed: {product.price} → {new_price}"
            event = Event(type="PRICE_CHANGE", message=message, product_id=product.id)
            db.add(event)
            if background_tasks: background_tasks.add_task(send_notification, message)
            product.price = new_price
            updated_count += 1
            
    db.commit()
    return {"total_checked": len(products), "updated": updated_count, "errors": errors}