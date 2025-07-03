"""Product model definition for the API."""

from pydantic import BaseModel, Field

class ProductModel(BaseModel):
    """Represents a product with its details."""
    productId: int = Field(alias="_id")
    name: str
    description: str
    price: float
    stock: int

    class Config:  # pylint: disable=too-few-public-methods
        """Pydantic configuration for ProductModel."""
        populate_by_name = True
        arbitrary_types_allowed = True