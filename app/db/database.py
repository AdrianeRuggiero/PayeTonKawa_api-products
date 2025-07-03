"""Database connection and collection setup for the products API."""
from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]

# Accès à la collection "products"
products_collection = db["products"]
