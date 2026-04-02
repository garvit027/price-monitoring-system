from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.routes import products
import time
from collections import defaultdict

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
async def add_auth_and_tracking(request: Request, call_next):
    # 🔓 Assignment Auth (Always Allow)
    client_ip = request.client.host
    consumer_id = request.headers.get("X-API-Key", client_ip)
    
    # Track usage
    usage_stats[consumer_id] += 1
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Usage-Count"] = str(usage_stats[consumer_id])
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Graceful handling of bad input or unexpected errors
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred.", "details": str(exc)},
    )


app.include_router(products.router, prefix="/api")