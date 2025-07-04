import pytest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from app.services import product_service
from app.models.product import ProductCreateModel, ProductModel

@pytest.fixture
def fake_product_data():
    return {
        "_id": str(ObjectId()),
        "name": "Test Product",
        "description": "A test product",
        "price": 9.99,
        "stock": 10,
        "category": "Test",
        "is_active": True
    }

@pytest.fixture
def fake_product_create():
    return ProductCreateModel(
        name="Test Product",
        description="A test product",
        price=9.99,
        stock=10,
        category="Test",
        is_active=True
    )

def test_create_product(fake_product_create, fake_product_data):
    with patch("app.services.product_service.products_collection") as mock_collection:
        mock_collection.insert_one.return_value.inserted_id = ObjectId(fake_product_data["_id"])
        result = product_service.create_product(fake_product_create)
        assert isinstance(result, ProductModel)
        assert result.name == fake_product_create.name
        mock_collection.insert_one.assert_called_once()

def test_get_product_found(fake_product_data):
    with patch("app.services.product_service.products_collection") as mock_collection:
        mock_collection.find_one.return_value = fake_product_data
        result = product_service.get_product(fake_product_data["_id"])
        assert result is not None
        assert result.name == fake_product_data["name"]

def test_get_product_not_found():
    with patch("app.services.product_service.products_collection") as mock_collection:
        mock_collection.find_one.return_value = None
        result = product_service.get_product(str(ObjectId()))
        assert result is None

def test_list_products(fake_product_data):
    with patch("app.services.product_service.products_collection") as mock_collection:
        mock_collection.find.return_value = [fake_product_data]
        result = product_service.list_products()
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].name == fake_product_data["name"]

def test_update_product_success(fake_product_create, fake_product_data):
    with patch("app.services.product_service.products_collection") as mock_collection:
        mock_collection.find_one_and_update.return_value = fake_product_data
        result = product_service.update_product(fake_product_data["_id"], fake_product_create)
        assert result is not None
        assert result.name == fake_product_create.name

def test_update_product_not_found(fake_product_create):
    with patch("app.services.product_service.products_collection") as mock_collection:
        mock_collection.find_one_and_update.return_value = None
        result = product_service.update_product(str(ObjectId()), fake_product_create)
        assert result is None

def test_delete_product_success():
    with patch("app.services.product_service.products_collection") as mock_collection:
        mock_collection.delete_one.return_value.deleted_count = 1
        result = product_service.delete_product(str(ObjectId()))
        assert result is True

def test_delete_product_failure():
    with patch("app.services.product_service.products_collection") as mock_collection:
        mock_collection.delete_one.return_value.deleted_count = 0
        result = product_service.delete_product(str(ObjectId()))
        assert result is False
