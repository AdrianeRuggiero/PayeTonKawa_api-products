import pytest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from app.models.product import ProductModel
from app.services.product_service import (
    create_product,
    get_product,
    list_products,
    update_product,
    delete_product,
)

@pytest.fixture
def sample_product():
    return ProductModel(
        name="Test Product",
        description="Test description",
        price=10.0,
        in_stock=True,
        category="Test"
    )

@patch("app.services.products_service.products_collection")
def test_create_product(mock_collection, sample_product):
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = ObjectId()
    mock_collection.insert_one.return_value = mock_insert_result

    result = create_product(sample_product)
    assert result.name == sample_product.name
    mock_collection.insert_one.assert_called_once()

@patch("app.services.products_service.products_collection")
def test_get_product_found(mock_collection, sample_product):
    product_id = str(ObjectId())
    sample_dict = sample_product.model_dump(by_alias=True)
    sample_dict["_id"] = ObjectId(product_id)

    mock_collection.find_one.return_value = sample_dict
    result = get_product(product_id)

    assert result is not None
    assert result.name == sample_product.name
    mock_collection.find_one.assert_called_once_with({"_id": ObjectId(product_id)})

@patch("app.services.products_service.products_collection")
def test_get_product_not_found(mock_collection):
    mock_collection.find_one.return_value = None
    result = get_product(str(ObjectId()))
    assert result is None

@patch("app.services.products_service.products_collection")
def test_list_products(mock_collection, sample_product):
    sample_dict = sample_product.model_dump(by_alias=True)
    sample_dict["_id"] = ObjectId()
    mock_collection.find.return_value = [sample_dict]

    results = list_products()
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0].name == sample_product.name

@patch("app.services.products_service.products_collection")
def test_update_product_success(mock_collection, sample_product):
    product_id = str(ObjectId())
    sample_dict = sample_product.model_dump(by_alias=True)
    sample_dict["_id"] = ObjectId(product_id)

    mock_collection.find_one_and_update.return_value = sample_dict

    updated = update_product(product_id, sample_product)
    assert updated is not None
    assert updated.name == sample_product.name
    mock_collection.find_one_and_update.assert_called_once()

@patch("app.services.products_service.products_collection")
def test_update_product_fail(mock_collection, sample_product):
    mock_collection.find_one_and_update.return_value = None
    result = update_product(str(ObjectId()), sample_product)
    assert result is None

@patch("app.services.products_service.products_collection")
def test_delete_product_success(mock_collection):
    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 1
    mock_collection.delete_one.return_value = mock_delete_result

    result = delete_product(str(ObjectId()))
    assert result is True

@patch("app.services.products_service.products_collection")
def test_delete_product_fail(mock_collection):
    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 0
    mock_collection.delete_one.return_value = mock_delete_result

    result = delete_product(str(ObjectId()))
    assert result is False
