"""
Routes for product management in the API.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.product import ProductModel
from app.services import product_service
from app.security.dependencies import get_current_user, role_required

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductModel])
async def get_all(_=Depends(get_current_user)):
    """
    Récupère la liste de tous les produits.
    """
    return await product_service.list_products()

@router.post("/", response_model=ProductModel, status_code=status.HTTP_201_CREATED)
async def create(product: ProductModel, _=Depends(role_required("admin"))):
    """
    Crée un nouveau produit.
    """
    return await product_service.create_product(product)

@router.get("/{product_id}", response_model=ProductModel)
async def get_by_id(product_id: int, _=Depends(get_current_user)):
    """
    Récupère un produit par son ID.
    """
    product = await product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductModel)
async def update(product_id: int, product: ProductModel, _=Depends(role_required("admin"))):
    """
    Met à jour un produit existant.
    """
    updated = await product_service.update_product(product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found or not modified")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(product_id: int, _=Depends(role_required("admin"))):
    """
    Supprime un produit par son ID.
    """
    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
