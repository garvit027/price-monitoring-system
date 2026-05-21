import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal
from app.models.product import Product

db = SessionLocal()
sources = db.query(Product.source).distinct().all()
for (src,) in sources:
    print(f"\n--- {src} ---")
    prods = db.query(Product).filter(Product.source == src).limit(5).all()
    for p in prods:
        print(f"Name: {p.name}")
        print(f"Brand: {p.brand} | Price: {p.price} | Image: {p.image}")
db.close()
