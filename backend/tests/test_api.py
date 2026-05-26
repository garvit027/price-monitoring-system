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
    assert response.json() == {
        "total_products": 0,
        "average_price": 0,
        "by_source": {},
        "by_category": {},
        "purchases_by_source": {},
    }

def test_refresh_data():
    response = client.post("/api/refresh")
    assert response.status_code == 200
    data = response.json()
    assert "updated" in data
    assert "total_checked" in data

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
    assert response.json() == []

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


def test_product_price_alert():
    from app.models.product import Product
    
    db = TestingSessionLocal()
    test_product = Product(
        name="Test Product",
        brand="Test Brand",
        category="Test Category",
        source="Test Source",
        external_id="TEST12345",
        price=100.0,
        image="http://example.com/image.jpg",
        url="http://example.com/product"
    )
    db.add(test_product)
    db.commit()
    db.refresh(test_product)
    db.close()

    response = client.get("/api/products")
    assert response.status_code == 200
    products = response.json()
    assert len(products) > 0
    product = products[0]
    
    # Set alert price
    alert_response = client.post(f"/api/products/{product['id']}/alert", json={"alert_price": 50.0})
    assert alert_response.status_code == 200
    assert alert_response.json()["alert_price"] == 50.0
    
    # Verify product has alert price now
    get_response = client.get(f"/api/products/{product['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["alert_price"] == 50.0

    # Clear alert price
    clear_response = client.post(f"/api/products/{product['id']}/alert", json={"alert_price": None})
    assert clear_response.status_code == 200
    assert clear_response.json()["alert_price"] is None

    # Verify cleared in DB
    get_response2 = client.get(f"/api/products/{product['id']}")
    assert get_response2.status_code == 200
    assert get_response2.json()["alert_price"] is None
