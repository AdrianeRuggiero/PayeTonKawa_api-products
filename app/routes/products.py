"""
Routes for product management in the API.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.product import ProductModel, ProductCreateModel
from app.services import product_service
from app.security.dependencies import get_current_user, role_required

router = APIRouter(tags=["Products"])

@router.get("/", response_model=List[ProductModel])
async def get_all_products(_=Depends(get_current_user)):
    """
    Retrieve the list of all products.
    """
    return product_service.list_products()

@router.post("/", response_model=ProductModel, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreateModel, _=Depends(role_required("admin"))):
    """
    Create a new product.
    """
    return product_service.create_product(product)

@router.get("/{product_id}", response_model=ProductModel)
async def get_product_by_id(product_id: str, _=Depends(get_current_user)):
    product = product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductModel)
async def update_product(product_id: str, product: ProductCreateModel, _=Depends(role_required("admin"))):
    """
    Update an existing product by its ID.
    """
    updated = product_service.update_product(product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found or not modified")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, _=Depends(role_required("admin"))):
    """
    Delete a product by its ID.
    """
    success = product_service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
