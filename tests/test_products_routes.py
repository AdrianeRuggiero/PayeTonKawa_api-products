from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.security.auth import create_access_token

client = TestClient(app)

def get_auth_headers(role="admin"):
    token = create_access_token({"sub": "testuser", "role": role})
    return {"Authorization": f"Bearer {token}"}

@patch("app.routes.products.publish_message")
def test_create_product(mock_publish):
    payload = {
        "name": "Test Product",
        "description": "Produit pour test",
        "price": 9.99,
        "in_stock": True,
        "category": "Test"
    }
    response = client.post("/products/", json=payload, headers=get_auth_headers())
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert "price" in data
    mock_publish.assert_called_once()

def test_list_products():
    response = client.get("/products/", headers=get_auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product():
    # Créer un produit pour récupérer son ID
    payload = {"name": "Produit Test", "price": 5.0}
    create_resp = client.post("/products/", json=payload, headers=get_auth_headers())
    product_id = create_resp.json()["_id"]

    get_resp = client.get(f"/products/{product_id}", headers=get_auth_headers())
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == payload["name"]

def test_update_product():
    payload = {"name": "Produit à modifier", "price": 3.0}
    create_resp = client.post("/products/", json=payload, headers=get_auth_headers())
    product_id = create_resp.json()["_id"]

    updated_payload = {"name": "Produit modifié", "price": 4.5, "in_stock": False}
    update_resp = client.put(f"/products/{product_id}", json=updated_payload, headers=get_auth_headers())
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == updated_payload["name"]
    assert update_resp.json()["in_stock"] == False

def test_delete_product():
    payload = {"name": "Produit à supprimer", "price": 1.0}
    create_resp = client.post("/products/", json=payload, headers=get_auth_headers())
    product_id = create_resp.json()["_id"]

    delete_resp = client.delete(f"/products/{product_id}", headers=get_auth_headers())
    assert delete_resp.status_code == 204

    # Vérifie que le produit est bien supprimé
    get_resp = client.get(f"/products/{product_id}", headers=get_auth_headers())
    assert get_resp.status_code == 404
