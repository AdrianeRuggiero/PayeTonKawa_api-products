from pydantic import BaseModel, Field

class ProductModel(BaseModel):
    productId: int = Field(alias="_id")
    name: str
    description: str
    price: float
    stock: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True