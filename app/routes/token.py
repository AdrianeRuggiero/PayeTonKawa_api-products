"""
This module defines the token route for user authentication and JWT token generation.
"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.security.auth import create_access_token

router = APIRouter()

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and returns a JWT access token with an assigned role.
    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
    Returns:
        dict: A dictionary containing the access token and its type.
    """
    # Authentification simplifiée : retourne un JWT avec un rôle
    if form_data.username == "admin":
        role = "admin"
    else:
        role = "user"

    token = create_access_token({"sub": form_data.username, "role": role})
    return {"access_token": token, "token_type": "bearer"}
