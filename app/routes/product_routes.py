from fastapi import APIRouter, HTTPException
from app.schemas.product_schema import ProductCreate
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def get_all():
    products = product_service.get_all_products()
    for p in products:
        p["_id"] = str(p["_id"])
    return products

@router.get("/{product_id}")
def get_by_id(product_id: str):
    product = product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product["_id"] = str(product["_id"])
    return product

@router.post("/")
def create(product: ProductCreate):
    product_id = product_service.create_product(product.dict())
    return {"id": str(product_id)}

@router.put("/{product_id}")
def update(product_id: str, product: ProductCreate):
    result = product_service.update_product(product_id, product.dict())
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated"}

@router.delete("/{product_id}")
def delete(product_id: str):
    result = product_service.delete_product(product_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}
