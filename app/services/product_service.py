"""
Service functions for managing products in the database.
"""

from app.db.database import products_collection as collection
from app.models.product import ProductModel

def list_products():
    """
    Récupère tous les produits de la base de données.
    Returns:
        List[ProductModel]: Liste des produits.
    """
    cursor = collection.find({})
    products = [ProductModel(**product) for product in cursor]
    return products

async def create_product(product: ProductModel):
    """
    Crée un nouveau produit dans la base de données.
    Args:
        product (ProductModel): Le produit à créer.
    Returns:
        ProductModel: Le produit créé avec son ID.
    """
    data = product.model_dump(by_alias=True)
    last = await collection.find_one(sort=[("_id", -1)])
    next_id = (last["_id"] + 1) if last else 1
    data["_id"] = next_id
    await collection.insert_one(data)
    new_product = await collection.find_one({"_id": next_id})
    return ProductModel(**new_product)

async def get_product(product_id: int):
    """
    Récupère un produit par son ID.
    Args:
        product_id (int): L'ID du produit à récupérer.
    Returns:
        ProductModel: Le produit correspondant à l'ID, ou None si non trouvé.
    """
    doc = await collection.find_one({"_id": product_id})
    return ProductModel(**doc) if doc else None

async def update_product(product_id: int, updated: ProductModel):
    """
    Met à jour un produit existant dans la base de données.
    Args:
        product_id (int): L'ID du produit à mettre à jour.
        updated (ProductModel): Le modèle de produit avec les nouvelles données.
    Returns:
        ProductModel: Le produit mis à jour, ou None si non trouvé.
    """
    data = updated.model_dump(by_alias=True, exclude={"productId"})
    result = await collection.update_one({"_id": product_id}, {"$set": data})
    if result.matched_count == 0:
        return None
    new_doc = await collection.find_one({"_id": product_id})
    return ProductModel(**new_doc)

async def delete_product(product_id: int):
    """
    Supprime un produit de la base de données par son ID.
    Args:
        product_id (int): L'ID du produit à supprimer.
    Returns:
        bool: True si la suppression a réussi, False sinon.
    """
    result = await collection.delete_one({"_id": product_id})
    return result.deleted_count > 0
