from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.models.event import Event
from app.services.loader import load_products
from app.services.parsers import get_parser
from app.services.normalizer import normalize
from app.services.notification import send_notification
from app.services.retry import retry

def ingest_products(db: Session):
    inserted = 0
    updated = 0

    for raw_data, filename in load_products():
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
            db.add(Product(**product_data))
            inserted += 1

        else:
            # 🔥 PRICE CHANGE DETECTION
            if existing.price != product_data["price"]:

                # 🧾 Save history
                history = PriceHistory(
                    product_id=existing.id,
                    old_price=existing.price,
                    new_price=product_data["price"]
                )
                db.add(history)

                # 🧾 Log event
                message = f"{existing.name} price changed from {existing.price} → {product_data['price']}"
                event = Event(
                    type="PRICE_CHANGE",
                    message=message
                )
                db.add(event)

                # 🔔 Notification with retry
                retry(lambda: send_notification(message))

                # update price
                existing.price = product_data["price"]
                updated += 1

    db.commit()

    return {
        "inserted": inserted,
        "updated": updated
    }