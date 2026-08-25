import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher

from app.core.database import SessionLocal


JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    try:
        return password_hasher.verify(
            hashed_password,
            password,
        )
    except Exception:
        return False


def create_access_token(
    user_id: int,
    user_type: str,
) -> str:

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "user_type": user_type,
        "iat": now,
        "exp": now + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()