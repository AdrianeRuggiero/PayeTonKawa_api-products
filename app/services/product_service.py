"""sumary_line

Keyword arguments:
argument -- description
Return: return_description
"""

from typing import List, Optional
from app.models.product import ProductModel, ProductCreateModel, PyObjectId
from app.db.database import products_collection
from bson import ObjectId

def create_product(product: ProductCreateModel) -> ProductModel:
    """
    Creates a new product in the database.
    Args:
        product (ProductCreateModel): The product data to be created.
    Returns:
        ProductModel: The created product with its ID.
    """
    product_dict = product.model_dump(by_alias=True, exclude_unset=True)
    result = products_collection.insert_one(product_dict)
    product_dict["_id"] = str(result.inserted_id)
    return ProductModel(**product_dict)

def get_product(product_id: str) -> Optional[ProductModel]:
    """Retrieves a product by its ID from the database.
    Args:
        product_id (str): The ID of the product to retrieve.
    Returns:        
        Optional[ProductModel]: The product if found, otherwise None.
    """
    if not ObjectId.is_valid(product_id):
        return None
    product_data = products_collection.find_one({"_id": ObjectId(product_id)})
    if product_data:
        product_data["_id"] = str(product_data["_id"])
        return ProductModel(**product_data)
    return None

def list_products() -> List[ProductModel]:
    """Lists all products in the database.
    Returns:
        List[ProductModel]: A list of all products.
    """ 
    products = []
    for doc in products_collection.find():
        doc["_id"] = str(doc["_id"])
        products.append(ProductModel(**doc))
    return products

def update_product(product_id: str, product: ProductCreateModel) -> Optional[ProductModel]:
    """Updates an existing product by its ID.
    Args:
        product_id (str): The ID of the product to update.
        product (ProductCreateModel): The updated product data.
    Returns:
        Optional[ProductModel]: The updated product if successful, otherwise None.
    """
    """Updates an existing product by its ID.   
    Args:
        product_id (str): The ID of the product to update.
        product (ProductCreateModel): The updated product data.     
    Returns:
        Optional[ProductModel]: The updated product if successful, otherwise None.
    """
    if not ObjectId.is_valid(product_id):
        return None
    update_data = product.model_dump(by_alias=True, exclude_unset=True)
    updated = products_collection.find_one_and_update(
        {"_id": ObjectId(product_id)},
        {"$set": update_data},
        return_document=True
    )
    if updated:
        updated["_id"] = str(updated["_id"])
        return ProductModel(**updated)
    return None

def delete_product(product_id: str) -> bool:
    """Deletes a product by its ID.
    Args:
        product_id (str): The ID of the product to delete.
    Returns:
        bool: True if the product was deleted, otherwise False.
    """
    if not ObjectId.is_valid(product_id):
        return False
    result = products_collection.delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count == 1
