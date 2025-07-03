from pydantic import BaseModel, Field

class ProductCreatedMessage(BaseModel):
    productId: int = Field(..., alias="_id")
    name: str
    description: str
    price: float
    stock: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class ProductUpdatedMessage(BaseModel):
    productId: int = Field(..., alias="_id")
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class ProductDeletedMessage(BaseModel):
    productId: int = Field(..., alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True