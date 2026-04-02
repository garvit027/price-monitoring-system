from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.models.event import Event
from app.services.loader import load_products
from app.services.parsers import get_parser
from app.services.normalizer import normalize
from app.services.notification import send_notification
from app.services.retry import retry

async def ingest_products(db: Session, background_tasks=None):
    inserted = 0
    updated = 0

    async for raw_data, filename in load_products():
        parser, source = get_parser(filename)

        if not parser:
            continue

        parsed = parser(raw_data)
        product_data = normalize(parsed, source, filename)

        existing = db.query(Product).filter(
            Product.external_id == product_data["external_id"],
            Product.source == product_data["source"]
        ).first()

        if not existing:
            product = Product(**product_data)
            db.add(product)
            db.commit() # commit earlier for ID
            db.refresh(product)
            
            # Save history for new product too
            history = PriceHistory(
                product_id=product.id,
                price=product.price
            )
            db.add(history)
            inserted += 1

        else:
            # 🔥 PRICE CHANGE DETECTION
            if existing.price != product_data["price"]:

                # 🧾 Save history
                history = PriceHistory(
                    product_id=existing.id,
                    price=product_data["price"]
                )
                db.add(history)

                # 🧾 Log event
                message = f"{existing.name} price changed from {existing.price} → {product_data['price']}"
                event = Event(
                    type="PRICE_CHANGE",
                    message=message,
                    product_id=existing.id
                )
                db.add(event)

                # 🔔 Notification (Non-blocking)
                if background_tasks:
                    background_tasks.add_task(send_notification, message)
                else:
                    await send_notification(message)

                # update price
                existing.price = product_data["price"]
                updated += 1

    db.commit()

    return {
        "inserted": inserted,
        "updated": updated
    }