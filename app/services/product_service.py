# product_service.py

fake_db = []

def get_all_products():
    return fake_db

def get_product_by_id(product_id):
    for p in fake_db:
        if p.get("id") == product_id:
            return p
    return None

def create_product(product):
    product["id"] = str(len(fake_db) + 1)
    fake_db.append(product)
    return product["id"]

def update_product(product_id, product):
    for idx, p in enumerate(fake_db):
        if p.get("id") == product_id:
            fake_db[idx] = product
            return True
    return False

def delete_product(product_id):
    global fake_db
    new_db = [p for p in fake_db if p.get("id") != product_id]
    if len(new_db) == len(fake_db):
        return False
    fake_db = new_db
    return True
# CODE A UTILISER Apres integration DB
# from app.database.connection import db
# from bson import ObjectId
#
# collection = db["products"]
#
# def get_all_products():
#     return list(collection.find())
#
# def get_product_by_id(product_id):
#     return collection.find_one({"_id": ObjectId(product_id)})
#
# def create_product(product):
#     return collection.insert_one(product).inserted_id
#
# def update_product(product_id, product):
#     return collection.update_one({"_id": ObjectId(product_id)}, {"$set": product})
#
# def delete_product(product_id):
#     return collection.delete_one({"_id": ObjectId(product_id)})
