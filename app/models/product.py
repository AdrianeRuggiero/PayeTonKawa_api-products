"""
# File: app/models/product.py
# FastAPI Pydantic models for product management.
# This module defines the data models for products, including validation and serialization.
"""
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler
from bson import ObjectId

# Compatibilité ObjectId pour Pydantic v2
class PyObjectId(ObjectId):
    """
    Custom type for MongoDB ObjectId to be used with Pydantic models.
    This class extends ObjectId to provide validation and serialization.
    It ensures that the ObjectId is valid and can be serialized to a string.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.no_info_after_validator_function(cls.validate, core_schema.str_schema())

    @classmethod
    def validate(cls, value):
        """
        Validate that the value is a valid ObjectId.
        """
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)

class ProductModel(BaseModel):
    """
    Pydantic model for a product in the system.
    This model includes fields for product details such as name, description, price, stock,
    category, and status. It also includes an optional ID field for MongoDB ObjectId.   
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category: Optional[str] = None
    is_active: bool = True

    class Config:
        """
        Pydantic configuration for the ProductModel.
        This configuration enables population by name, sets JSON encoders for ObjectId,
        and provides an example schema for API documentation.
        """
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Café Arabica",
                "description": "Café 100% Arabica en grains",
                "price": 12.5,
                "stock": 100,
                "category": "Boissons",
                "is_active": True
            }
        }

class ProductCreateModel(BaseModel):
    """
    Pydantic model for creating a new product.
    This model includes fields for product details such as name, description, price, stock,
    category, and status. It does not include the ID field, as it is intended for creation only.
    """
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category: Optional[str] = None
    is_active: bool = True

    class Config:
        """
        Pydantic configuration for the ProductCreateModel.
        This configuration enables population by name and provides an example schema for API documentation.
        """
        json_schema_extra = {
            "example": {
                "name": "Café Arabica",
                "description": "Café 100% Arabica en grains",
                "price": 12.5,
                "stock": 100,
                "category": "Boissons",
                "is_active": True
            }
        }
