from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.product import ProductModel
from app.services.product_service import (
    create_product, get_product, list_products, update_product, delete_product
)
from fastapi import Depends
from app.security.dependencies import get_current_user, role_required

router = APIRouter()

@router.post("/", response_model=ProductModel, status_code=status.HTTP_201_CREATED)
def create(product: ProductModel, user=Depends(role_required("admin"))):
    """
    Endpoint : POST /products/
    - Crée un nouveau produit
    - Accessible uniquement aux admins
    - Valide avec ProductModel
    - Retourne le produit créé
    """
    return create_product(product)

@router.get("/", response_model=List[ProductModel], dependencies=[Depends(role_required("admin"))])
def get_all(user=Depends(get_current_user)):
    """
    Endpoint : GET /products/
    - Liste tous les produits
    - Accessible uniquement aux admins
    """
    return list_products()

@router.get("/{product_id}", response_model=ProductModel)
def get_by_id(product_id: str, user=Depends(get_current_user)):
    """
    Endpoint : GET /products/{product_id}
    - Récupère un produit par son ID
    - Accessible à tous les utilisateurs authentifiés
    """
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product

@router.put("/{product_id}", response_model=ProductModel)
def update(product_id: str, product: ProductModel, user=Depends(role_required("admin"))):
    """
    Endpoint : PUT /products/{product_id}
    - Met à jour un produit existant
    - Accessible uniquement aux admins
    """
    updated = update_product(product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Produit non trouvé ou non modifié")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(product_id: str, user=Depends(role_required("admin"))):
    """
    Endpoint : DELETE /products/{product_id}
    - Supprime un produit par son ID
    - Accessible uniquement aux admins
    - Retourne 204 si succès
    """
    success = delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return {"detail": "Produit supprimé avec succès"}
@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """
    Endpoint : GET /products/health
    - Vérifie la santé de l'API Products
    - Retourne 200 OK si l'API est opérationnelle
    """
    return {"status": "ok", "message": "API Products is healthy"}