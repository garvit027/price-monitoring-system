"""
Seed the PostgreSQL database with sample products from multiple marketplaces.
Run: python seed_db.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal, engine
from app.db.base import Base
import app.models  # ensure all models are registered
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.models.event import Event
from datetime import datetime, timedelta
import random

Base.metadata.create_all(bind=engine)

SEED_PRODUCTS = [
    # Amazon Products
    {
        "name": "Apple AirPods Pro (2nd Gen) - MagSafe Charging Case",
        "brand": "Apple", "category": "Electronics", "source": "Amazon",
        "external_id": "B0BDHWDR12", "price": 189.99,
        "image": "https://m.media-amazon.com/images/I/71zny68+7xL._AC_SX466_.jpg",
        "url": "https://www.amazon.com/dp/B0BDHWDR12"
    },
    {
        "name": "Samsung Galaxy S24 Ultra 512GB - Titanium Black",
        "brand": "Samsung", "category": "Electronics", "source": "Amazon",
        "external_id": "B0CMDRKPB7", "price": 1199.99,
        "image": "https://m.media-amazon.com/images/I/71hJWMpCIFL._AC_SX466_.jpg",
        "url": "https://www.amazon.com/dp/B0CMDRKPB7"
    },
    {
        "name": "Sony WH-1000XM5 Wireless Noise-Canceling Headphones",
        "brand": "Sony", "category": "Electronics", "source": "Amazon",
        "external_id": "B09XS7JWHH", "price": 279.99,
        "image": "https://m.media-amazon.com/images/I/51aXvjzcukL._AC_SX466_.jpg",
        "url": "https://www.amazon.com/dp/B09XS7JWHH"
    },
    {
        "name": "Apple MacBook Air 15-inch M3 Chip 2024 - Midnight",
        "brand": "Apple", "category": "Laptops", "source": "Amazon",
        "external_id": "B0CX235MK3", "price": 1299.99,
        "image": "https://m.media-amazon.com/images/I/71vFKBpKakL._AC_SX466_.jpg",
        "url": "https://www.amazon.com/dp/B0CX235MK3"
    },
    {
        "name": "Logitech MX Master 3S Wireless Mouse",
        "brand": "Logitech", "category": "Electronics", "source": "Amazon",
        "external_id": "B09HM94VDS", "price": 79.99,
        "image": "https://m.media-amazon.com/images/I/61ni3t1ryQL._AC_SX466_.jpg",
        "url": "https://www.amazon.com/dp/B09HM94VDS"
    },
    {
        "name": "iPad Pro 13-inch M4 256GB WiFi - Space Black",
        "brand": "Apple", "category": "Tablets", "source": "Amazon",
        "external_id": "B0D3J5RQZX", "price": 1099.99,
        "image": "https://m.media-amazon.com/images/I/71ANjmjebCL._AC_SX466_.jpg",
        "url": "https://www.amazon.com/dp/B0D3J5RQZX"
    },
    {
        "name": "DJI Mini 4 Pro Drone with RC 2 Controller",
        "brand": "DJI", "category": "Electronics", "source": "Amazon",
        "external_id": "B0CG9P6KNZ", "price": 959.00,
        "image": "https://m.media-amazon.com/images/I/61RJBCdDd2L._AC_SX466_.jpg",
        "url": "https://www.amazon.com/dp/B0CG9P6KNZ"
    },

    # Flipkart Products (prices in INR)
    {
        "name": "OnePlus 12 5G 256GB - Silky Black",
        "brand": "OnePlus", "category": "Smartphones", "source": "Flipkart",
        "external_id": "MOBGZSTFZFUYAZMK", "price": 64999.0,
        "image": "https://rukminim2.fliximg.com/image/416/416/xif0q/mobile/l/u/h/-original-imagzghz4fttuzsd.jpeg?q=70",
        "url": "https://www.flipkart.com/oneplus-12-5g-silky-black-256-gb/p/itmd4ce4d98c0b1b"
    },
    {
        "name": "Samsung 55-inch 4K QLED Smart TV QE55Q60C",
        "brand": "Samsung", "category": "TVs", "source": "Flipkart",
        "external_id": "TVSGZHYRZBQ3GHEY", "price": 54990.0,
        "image": "https://rukminim2.fliximg.com/image/416/416/xif0q/television/q/t/b/-original-imag7fef5y4pjgry.jpeg?q=70",
        "url": "https://www.flipkart.com/samsung-139cm-55-inch-qled-ultra-hd-4k-smart-tizen-tv/p/itm4da1ba5f8f4e6"
    },
    {
        "name": "Apple iPhone 15 128GB - Pink",
        "brand": "Apple", "category": "Smartphones", "source": "Flipkart",
        "external_id": "MOBGMJYS8HXNZBZF", "price": 72999.0,
        "image": "https://rukminim2.fliximg.com/image/416/416/xif0q/mobile/w/q/r/-original-imagz7yyzhg3bvq7.jpeg?q=70",
        "url": "https://www.flipkart.com/apple-iphone-15-pink-128-gb/p/itm6ac6485515ae4"
    },
    {
        "name": "boAt Rockerz 450 Bluetooth Wireless Headphone",
        "brand": "boAt", "category": "Audio", "source": "Flipkart",
        "external_id": "ACCFYGYXMJ7CZWGU", "price": 1299.0,
        "image": "https://rukminim2.fliximg.com/image/416/416/kplt4y80/headphone/t/r/j/rockerz-450-boat-original-imafyhfyfswhzmh9.jpeg?q=70",
        "url": "https://www.flipkart.com/boat-rockerz-450-bluetooth-headphone/p/itma43c87a8d8fcf"
    },
    {
        "name": "Xiaomi Smart Band 8 Pro Fitness Tracker",
        "brand": "Xiaomi", "category": "Wearables", "source": "Flipkart",
        "external_id": "SMWGYJ5ZGSZHYFHZ", "price": 5999.0,
        "image": "https://rukminim2.fliximg.com/image/416/416/xif0q/smartwatch-tracker/z/z/e/-original-imagzfdfjzcxbgsz.jpeg?q=70",
        "url": "https://www.flipkart.com/xiaomi-smart-band-8-pro/p/itm7bcb77c1ad4b8"
    },

    # Grailed Products
    {
        "name": "Palace Skateboards Tri-Ferg Logo Hoodie - Black",
        "brand": "Palace", "category": "Streetwear", "source": "Grailed",
        "external_id": "GR-12345", "price": 175.0,
        "image": "https://media-photos.depop.com/b1/24820268/1700039285_63f4e0aba23541c9b1fa4f49538e6ee2/P0.jpg",
        "url": "https://www.grailed.com/listings/12345"
    },
    {
        "name": "Supreme Box Logo Crewneck FW23 - Navy",
        "brand": "Supreme", "category": "Streetwear", "source": "Grailed",
        "external_id": "GR-23456", "price": 380.0,
        "image": "https://i.ebayimg.com/images/g/mHQAAOSwLPljQkM1/s-l1600.jpg",
        "url": "https://www.grailed.com/listings/23456"
    },
    {
        "name": "Comme des Garçons PLAY Heart Logo T-Shirt",
        "brand": "CDG PLAY", "category": "T-Shirts", "source": "Grailed",
        "external_id": "GR-34567", "price": 95.0,
        "image": "https://assets.grailed.com/1234/abcd.jpg",
        "url": "https://www.grailed.com/listings/34567"
    },

    # Fashionphile Products
    {
        "name": "Louis Vuitton Neverfull MM Monogram Canvas Tote",
        "brand": "Louis Vuitton", "category": "Handbags", "source": "Fashionphile",
        "external_id": "FP-55001", "price": 1450.0,
        "image": "https://images.fashionphile.com/images/LV-Neverfull.jpg",
        "url": "https://www.fashionphile.com/products/louis-vuitton-neverfull-mm"
    },
    {
        "name": "Chanel Classic Double Flap Bag - Caviar Black",
        "brand": "Chanel", "category": "Handbags", "source": "Fashionphile",
        "external_id": "FP-66002", "price": 8500.0,
        "image": "https://images.fashionphile.com/images/chanel-double-flap.jpg",
        "url": "https://www.fashionphile.com/products/chanel-classic-double-flap"
    },
    {
        "name": "Gucci GG Marmont Mini Shoulder Bag - Matelassé",
        "brand": "Gucci", "category": "Handbags", "source": "Fashionphile",
        "external_id": "FP-77003", "price": 850.0,
        "image": "https://images.fashionphile.com/images/gucci-marmont.jpg",
        "url": "https://www.fashionphile.com/products/gucci-gg-marmont-mini"
    },

    # 1stDibs Products
    {
        "name": "Vintage Rolex Submariner 1680 Tropical Dial",
        "brand": "Rolex", "category": "Watches", "source": "1stdibs",
        "external_id": "1D-44001", "price": 18500.0,
        "image": "https://a.1stdibscdn.com/rolex-submariner.jpg",
        "url": "https://www.1stdibs.com/fashion/watches/id-v_001"
    },
    {
        "name": "Hermès Birkin 35 Togo Leather - Gold",
        "brand": "Hermès", "category": "Handbags", "source": "1stdibs",
        "external_id": "1D-55002", "price": 24000.0,
        "image": "https://a.1stdibscdn.com/hermes-birkin.jpg",
        "url": "https://www.1stdibs.com/fashion/handbags/id-v_002"
    },
]


def seed():
    db = SessionLocal()
    try:
        existing_count = db.query(Product).count()
        print(f"Existing products: {existing_count}")

        seeded = 0
        for p_data in SEED_PRODUCTS:
            existing = db.query(Product).filter(
                Product.external_id == p_data["external_id"],
                Product.source == p_data["source"]
            ).first()

            if existing:
                print(f"  ↩️  Skipping existing: {p_data['name'][:50]}")
                continue

            product = Product(**p_data)
            db.add(product)
            db.commit()
            db.refresh(product)

            # Create realistic price history (last 30 days)
            base_price = p_data["price"]
            for days_ago in range(30, 0, -1):
                fluctuation = random.uniform(-0.08, 0.08)
                hist_price = round(base_price * (1 + fluctuation), 2)
                hist = PriceHistory(
                    product_id=product.id,
                    price=hist_price,
                    timestamp=datetime.utcnow() - timedelta(days=days_ago)
                )
                db.add(hist)

            # Add current price
            db.add(PriceHistory(product_id=product.id, price=base_price))
            db.commit()

            seeded += 1
            print(f"  ✅ Seeded: {p_data['name'][:60]} @ ${base_price}")

        print(f"\n🚀 Done! Seeded {seeded} new products.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
