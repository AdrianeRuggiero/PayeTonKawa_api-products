"""
FastAPI application entry point for managing products and authentication.

This module initializes the FastAPI app, includes routers for product management and token
authentication, and provides a RESTful API for CRUD operations on products. The application uses
MongoDB for data storage and JWT for authentication, ensuring secure and efficient API endpoints
with proper error handling.
"""

from fastapi import FastAPI
from app.routes import products, token

app = FastAPI()

app.include_router(token.router)
app.include_router(products.router, prefix="/products", tags=["products"])
