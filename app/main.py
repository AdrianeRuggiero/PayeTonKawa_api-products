import sys
import os
from fastapi import FastAPI
from app.routes import product_routes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="Product API")

app.include_router(product_routes.router)
