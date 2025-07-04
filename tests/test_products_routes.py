import pytest
from fastapi.testclient import TestClient
from bson import ObjectId
from unittest.mock import patch
from app.main import app
from app.security import dependencies

# ✅ Overrides de sécurité
# Toutes les routes exigent un user authentifié, certaines exigent "admin"

def override_get_current_user():
    # Simuler un utilisateur toujours "admin" pour tout
    return {"username": "testuser", "role": "admin"}

def override_role_required(role):
    # Retourne une dépendance synchrone valide
    def fake_dependency():
        return {"username": "testuser", "role": role}
    return fake_dependency

app.dependency_overrides[dependencies.get_current_user] = override_get_current_user
app.dependency_overrides[dependencies.role_required] = override_role_required

client = TestClient(app)

# ✅ Fixture de produit factice
@pytest.fixture
def fake_product():
    return {
        "_id": str(ObjectId()),
        "name": "Test Product",
        "description": "A test product",
        "price": 9.99,
        "stock": 10,
        "category": "Test",
        "is_active": True
    }

# ✅ TEST GET ALL
def test_get_all_products(fake_product):
    with patch("app.services.product_service.list_products", return_value=[fake_product]):
        response = client.get("/products/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["name"] == "Test Product"

# ✅ TEST POST (CREATE)
def test_create_product(fake_product):
    with patch("app.services.product_service.create_product", return_value=fake_product):
        response = client.post("/products/", json={
            "name": "Test Product",
            "description": "A test product",
            "price": 9.99,
            "stock": 10,
            "category": "Test",
            "is_active": True
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Product"

# ✅ TEST GET BY ID
def test_get_product_by_id_found(fake_product):
    with patch("app.services.product_service.get_product", return_value=fake_product):
        response = client.get(f"/products/{fake_product['_id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Product"

def test_get_product_by_id_not_found():
    with patch("app.services.product_service.get_product", return_value=None):
        response = client.get(f"/products/{str(ObjectId())}")
        assert response.status_code == 404

# ✅ TEST PUT (UPDATE)
def test_update_product_success(fake_product):
    with patch("app.services.product_service.update_product", return_value=fake_product):
        response = client.put(f"/products/{fake_product['_id']}", json={
            "name": "Updated Product",
            "description": "Updated description",
            "price": 19.99,
            "stock": 5,
            "category": "Updated",
            "is_active": False
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Product"

def test_update_product_not_found():
    with patch("app.services.product_service.update_product", return_value=None):
        response = client.put(f"/products/{str(ObjectId())}", json={
            "name": "Nonexistent Product",
            "price": 19.99,
            "stock": 5
        })
        assert response.status_code == 404

# ✅ TEST DELETE
def test_delete_product_success():
    with patch("app.services.product_service.delete_product", return_value=True):
        response = client.delete(f"/products/{str(ObjectId())}")
        assert response.status_code == 204

def test_delete_product_not_found():
    with patch("app.services.product_service.delete_product", return_value=False):
        response = client.delete(f"/products/{str(ObjectId())}")
        assert response.status_code == 404
