from fastapi import FastAPI
from app.routes import products, token

app = FastAPI()
"""_summary_
    FastAPI application for managing products.
    This application provides endpoints to create, read, update, and delete products.
    It also includes authentication endpoints for token generation.
    The application uses MongoDB for data storage and JWT for authentication.
    The API is designed to be secure and efficient, with proper error handling and response formatting."""
app.include_router(token.router)
app.include_router(products.router, prefix="/products", tags=["products"])
