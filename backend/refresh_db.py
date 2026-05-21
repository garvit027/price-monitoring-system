import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.models.event import Event
from app.services.ingestion import auto_discover_and_grow

async def refresh():
    db = SessionLocal()
    try:
        print("Wiping fake seeded data...")
        db.query(PriceHistory).delete()
        db.query(Event).delete()
        db.query(Product).delete()
        db.commit()
        
        print("Discovering REAL products via Web Scraping (this may take a minute)...")
        result = await auto_discover_and_grow(db)
        print(f"Success! Discovered and scraped {result['new_discovered']} real products with valid images.")
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(refresh())
