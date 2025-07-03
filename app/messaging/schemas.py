"""Schemas for product messaging events."""

from pydantic import BaseModel, Field

class ProductCreatedMessage(BaseModel):
    """Message schema for a created product event."""
    productId: int = Field(..., alias="_id")
    name: str
    description: str
    price: float
    stock: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class ProductUpdatedMessage(BaseModel):
    """Message schema for an updated product event."""
    productId: int = Field(..., alias="_id")
    name: str | None = None
    description: str | None = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class ProductDeletedMessage(BaseModel):
    """Message schema for a deleted product event."""
    productId: int = Field(..., alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
