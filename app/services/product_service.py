from typing import List, Optional
from app.models.product import ProductModel, PyObjectId
from app.db.database import products_collection
from bson import ObjectId
from app.messaging.producer import publish_message  # ← Import RabbitMQ publisher

def create_product(product: ProductModel) -> ProductModel:
    """
    Crée un nouveau produit dans la base de données.
    Publie un message RabbitMQ après la création du produit.
    :param product: Instance de ProductModel à créer.
    :return: Instance de ProductModel créée avec l'ID généré par MongoDB.
    """
    # Convertir le modèle en dictionnaire pour l'insertion dans MongoDB
    # Utiliser by_alias pour respecter les alias définis dans le modèle
    product_dict = product.model_dump(by_alias=True, exclude_unset=True)
    result = products_collection.insert_one(product_dict)
    product_dict["_id"] = str(result.inserted_id)

    # Publier un message RabbitMQ après création du produit
    publish_message("product_events", f"Product created: {product_dict['_id']}")

    return ProductModel(**product_dict)

def get_product(product_id: str) -> Optional[ProductModel]:
    """
    Récupère un produit par son ID.
    :param product_id: ID du produit à récupérer.
    :return: Instance de ProductModel si trouvé, sinon None.
    """
    if not ObjectId.is_valid(product_id):
        return None
    product_data = products_collection.find_one({"_id": ObjectId(product_id)})
    if product_data:
        product_data["_id"] = str(product_data["_id"])
        return ProductModel(**product_data)
    return None

def list_products() -> List[ProductModel]:
    """
    Récupère tous les produits de la base de données.
    :return: Liste de ProductModel contenant tous les produits.
    """
    products = []
    for doc in products_collection.find():
        doc["_id"] = str(doc["_id"])
        products.append(ProductModel(**doc))
    return products

def update_product(product_id: str, product: ProductModel) -> Optional[ProductModel]:
    """
    Met à jour un produit existant.
    :param product_id: ID du produit à mettre à jour.
    :param product: Instance de ProductModel avec les données mises à jour.
    :return: Instance de ProductModel mise à jour si le produit a été trouvé et modifié, sinon None.
    """
     # Vérifier si l'ID du produit est valide
     # Si l'ID n'est pas valide, retourner None
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
    """Supprime un produit par son ID.
    :param product_id: ID du produit à supprimer.
    :return: True si le produit a été supprimé, sinon False.
    """
    if not ObjectId.is_valid(product_id):
        return False
    result = products_collection.delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count == 1
