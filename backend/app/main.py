from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.routes import products
from app.routes import auth as auth_router
import app.models  # ensure all models are imported for table creation
import asyncio
import time
from collections import defaultdict
from app.services.ingestion import auto_discover_and_grow
from app.db.session import SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Price Monitoring System")

# Simple usage tracking (in-memory)
usage_stats = defaultdict(int)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_tracking(request: Request, call_next):
    client_ip = request.client.host
    consumer_id = request.headers.get("X-API-Key", client_ip)
    usage_stats[consumer_id] += 1

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Usage-Count"] = str(usage_stats[consumer_id])
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred.", "details": str(exc)},
    )


# Mount routers
app.include_router(products.router, prefix="/api")
app.include_router(auth_router.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}


async def periodic_worker():
    """
    Background worker that runs every 5 minutes to:
    1. Discover new products from the web.
    2. Sync prices for existing products.
    3. Remove old products to maintain the limit.
    """
    while True:
        db = SessionLocal()
        try:
            print("🚀 Starting background discovery and sync loop...")
            result = await auto_discover_and_grow(db)
            print(f"✅ Periodic sync complete: {result}")
        except Exception as e:
            print(f"❌ Periodic sync failed: {e}")
        finally:
            db.close()

        # Run every 5 minutes
        await asyncio.sleep(300)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_worker())
    print("✅ Background worker initialized. Monitoring price changes...")