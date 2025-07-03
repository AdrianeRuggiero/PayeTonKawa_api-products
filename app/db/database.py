from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]

# Accès à la collection "products"
products_collection = db["products"]
print("Bases de données disponibles :")
print(client.list_database_names())

print("Collections dans products_db :")
print(db.list_collection_names())