from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool
