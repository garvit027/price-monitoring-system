import asyncio
from app.db.session import SessionLocal
from app.services.ingestion import sync_real_time_data
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    db = SessionLocal()
    try:
        print("Starting real-time sync test...")
        result = await sync_real_time_data(db)
        print(f"Sync Results: {result}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
