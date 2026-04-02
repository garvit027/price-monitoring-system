import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.routes.products import get_db

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_products.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup():
    # Setup
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown

def test_read_analytics_empty():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    assert response.json() == {"total_products": 0, "average_price": 0}

def test_refresh_data():
    response = client.post("/api/refresh")
    assert response.status_code == 200
    data = response.json()
    assert "inserted" in data

def test_get_products():
    client.post("/api/refresh")
    response = client.get("/api/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_product_not_found():
    response = client.get("/api/products/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_price_history_empty():
    response = client.get("/api/products/9999/history")
    assert response.status_code == 200
    assert response.json() == {"message": "No price history found"}

def test_cors_headers():
    response = client.get("/api/products", headers={"Origin": "http://localhost:5173"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

def test_usage_tracking_headers():
    response = client.get("/api/analytics", headers={"X-API-Key": "test-key"})
    assert response.status_code == 200
    assert "x-process-time" in response.headers
    assert "x-usage-count" in response.headers
    
    response2 = client.get("/api/analytics", headers={"X-API-Key": "test-key"})
    assert int(response2.headers["x-usage-count"]) == int(response.headers["x-usage-count"]) + 1

def test_products_with_filter():
    client.post("/api/refresh")
    response = client.get("/api/products?source=Grailed")
    assert response.status_code == 200
    for product in response.json():
        assert product["source"] == "Grailed"
