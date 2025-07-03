from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.product import ProductModel
from app.services import product_service
from app.security.dependencies import get_current_user, role_required


router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductModel])
async def get_all(user=Depends(get_current_user)):
    """
    Récupère la liste de tous les produits.
    - user: dépendance pour récupérer l'utilisateur actuel (authentifié)
    - Retourne une liste de produits
    """

    return await product_service.list_products()

@router.post("/", response_model=ProductModel, status_code=status.HTTP_201_CREATED)
async def create(product: ProductModel, user=Depends(role_required("admin"))):
    """
    Crée un nouveau produit.
    - product: modèle de produit à créer
    - user: dépendance pour vérifier que l'utilisateur a le rôle 'admin'
    - Retourne le produit créé
    """
    return await product_service.create_product(product)

@router.get("/{product_id}", response_model=ProductModel)
async def get_by_id(product_id: int, user=Depends(get_current_user)):
    """
    Récupère un produit par son ID.
    - product_id: ID du produit à récupérer
    - user: dépendance pour récupérer l'utilisateur actuel (authentifié)
    - Retourne le produit correspondant à l'ID
    """
    product = await product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductModel)
async def update(product_id: int, product: ProductModel, user=Depends(role_required("admin"))):
    """
    Met à jour un produit existant.
    - product_id: ID du produit à mettre à jour
    - product: modèle de produit avec les nouvelles données
    - user: dépendance pour vérifier que l'utilisateur a le rôle 'admin'
    - Retourne le produit mis à jour
    """
    updated = await product_service.update_product(product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found or not modified")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(product_id: int, user=Depends(role_required("admin"))):
    """
    Supprime un produit par son ID.
    - product_id: ID du produit à supprimer
    - user: dépendance pour vérifier que l'utilisateur a le rôle 'admin'
    - Retourne un statut 204 No Content si la suppression est réussie
    """
    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
