from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.security.auth import create_access_token

router = APIRouter()

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint : POST /token
    - Authentifie l’utilisateur (ici simplifié)
    - Retourne un JWT contenant le username et le rôle
    """
    # Simplified authentication logic
    if form_data.username == "admin" and form_data.password == "adminpassword":   
        role = "admin"
    elif form_data.username and form_data.password:
        role = "user"
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create JWT token with username and role
    token = create_access_token({"sub": form_data.username, "role": role})
    return {"access_token": token, "token_type": "bearer"}
