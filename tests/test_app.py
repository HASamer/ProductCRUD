import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "the root endpoint is working!"}

def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_product():
    product_data = {"name": "Test Product", "quantity": "10", "category": "Test Category"}
    response = client.post("/products/", json=product_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"

def test_get_product_by_id():
    product_id = str(uuid.uuid4())
    response = client.get(f"/products/{product_id}")
    assert response.status_code in [200, 404]

def test_update_product():
    product_id = str(uuid.uuid4())
    updated_data = {"name": "Updated Product", "quantity": "15"}
    response = client.put(f"/products/{product_id}", json=updated_data)
    assert response.status_code in [200, 404]

def test_delete_product():
    product_id = str(uuid.uuid4())
    response = client.delete(f"/products/{product_id}")
    assert response.status_code in [200, 404]