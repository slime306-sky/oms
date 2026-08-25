import jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import get_db
from app.core.security import (
    JWT_ALGORITHM,
    JWT_SECRET,
)

from app.database.models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def get_current_user(
    access_token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:

    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid access token")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid access token")

    user = db.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_current_user_optional(
    access_token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User | None:
    if not access_token:
        return None
    try:
        payload = jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            return None
        return db.get(User, int(user_id))
    except jwt.PyJWTError:
        return None

def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Only allows main admins through. Use on admin-only endpoints."""
    if current_user.main_admin is None:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


def require_admin_or_self(
    user_id: int,
    current_user: User = Depends(get_current_user),
) -> User:
    """Allows an admin, or the user accessing their own resource."""
    is_admin = current_user.main_admin is not None
    is_self = current_user.id == user_id
    if not (is_admin or is_self):
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    return current_user