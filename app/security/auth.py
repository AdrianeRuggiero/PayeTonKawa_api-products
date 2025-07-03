"""Authentication utilities for JWT token creation and verification."""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from app.config import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with an expiration time.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (Optional[timedelta]): The time delta for token expiration.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """
    Verify a JWT token and return its payload if valid.

    Args:
        token (str): The JWT token to verify.

    Returns:
        dict or None: The decoded payload if valid, otherwise None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None