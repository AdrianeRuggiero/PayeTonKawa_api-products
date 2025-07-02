from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.security.auth import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Récupère l'utilisateur actuel à partir du token JWT.
    - token: JWT passé dans l'en-tête Authorization
    - Retourne le payload du token si valide, sinon 401 Unauthorized
    """
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

def role_required(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        """
        Vérifie que l'utilisateur a le rôle requis.
        - required_role: rôle à vérifier (ex: "admin")
        - user: payload extrait du token JWT
        - Lève 403 Forbidden si rôle non autorisé
        """
        if user.get("role") != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès interdit")
        return user
    return role_checker
