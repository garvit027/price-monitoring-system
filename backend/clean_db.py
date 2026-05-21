import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal
from app.models.product import Product
from app.models.price_history import PriceHistory

db = SessionLocal()

# Find bad products
bad_products = db.query(Product).filter(
    (Product.price == 0) | 
    (Product.price == None) | 
    (Product.image == None) | 
    (Product.name == "Unknown Product")
).all()

count = len(bad_products)
for p in bad_products:
    db.query(PriceHistory).filter(PriceHistory.product_id == p.id).delete()
    db.delete(p)

db.commit()
print(f"Deleted {count} broken products (missing images, 0 prices, or captchas).")
db.close()
