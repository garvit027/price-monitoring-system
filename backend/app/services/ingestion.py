from sqlalchemy.orm import Session
from app.models.product import Product
from app.services.loader import load_products
from app.services.parsers import get_parser
from app.services.normalizer import normalize

def ingest_products(db: Session):
    inserted = 0

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

    db.commit()
    return inserted