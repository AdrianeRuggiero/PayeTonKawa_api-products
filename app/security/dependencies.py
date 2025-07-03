"""
This module provides security-related dependencies for FastAPI routes,
including role-based access control.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.security.auth import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieves the current user from the provided JWT token.

    Args:
        token (str): The JWT token from the request.

    Returns:
        dict: The payload containing user information.

    Raises:
        HTTPException: If the token is invalid.
    """
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )
    return payload

def role_required(required_role: str):
    """
    Dependency factory that ensures the current user has the specified role.

    Args:
        required_role (str): The role required to access the endpoint.

    Returns:
        Callable: A dependency function for FastAPI that checks the user's role.

    Raises:
        HTTPException: If the current user's role does not match the required role,
        a 403 Forbidden error is raised.
    """
    def role_checker(user=Depends(get_current_user)):
        """
        Checks if the current user's role matches the required role.

        Args:
            user (dict): The current user object, expected to have a 'role' key.

        Returns:
            dict: The user object if the role matches.

        Raises:
            HTTPException: If the user's role does not match the required role.
        """
        if user.get("role") != required_role:
            raise HTTPException(
                status_code=403,
                detail="Accès interdit"
            )
        return user
    return role_checker
