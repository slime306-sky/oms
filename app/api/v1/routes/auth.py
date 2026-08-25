from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Response
from fastapi.params import Cookie
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import api_error
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
    get_db,
)

from app.database.models.employee import Gender, RoleName
from app.database.models.users import User, UserType
from app.database.models.main_admin import MainAdmin
from app.database.models.refresh_token import RefreshToken

from app.schema.auth import LoginRequest, RegisterRequest
from app.services.auth import register_employee, update_employee_id
from app.services.auth_dependencies import require_admin


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    existing_user = db.scalar(
        select(User).where(
            (User.email == data.email) | (User.username == data.username)
        )
    )

    if existing_user:
        raise api_error(
            status_code=409,
            code="ALREADY_EXISTS",
            message="A user with this username or email already exists",
        )

    if data.user_type == UserType.EMPLOYEE and not data.employee:
        raise api_error(
            status_code=400,
            code="MORE_INFORMATION_IS_NEEDED",
            message="Employee information is required",
        )

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        user_type=data.user_type,
    )

    if data.user_type == UserType.EMPLOYEE:
        user.employee = register_employee(data, db)
    elif data.user_type == UserType.MAIN_ADMIN:
        user.main_admin = MainAdmin()

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise

    if data.user_type == UserType.EMPLOYEE:
        update_employee_id(user, db)
        db.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "username": user.username,
        "user_type": user.user_type.value,
        "employee_id": user.employee.employee_id if user.employee else None,
    }


@router.get("/register")
def get_register_enums(current_user: User = Depends(require_admin)):
    return {
        "user_type": [e.value for e in UserType],
        "role": [e.value for e in RoleName],
        "gender": [e.value for e in Gender],
    }

@router.post("/login")
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    user = db.scalar(select(User).where(User.email == data.email))

    if not user or not verify_password(data.password, user.hashed_password):
        raise api_error(
            status_code=401,
            code="INVALID_CREDENTIALS",
            message="Invalid email or password",
        )

    access_token = create_access_token(user_id=user.id, user_type=user.user_type.value)
    refresh_token = create_refresh_token()
    now = datetime.now(timezone.utc)

    refresh_token_record = RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(refresh_token),
        created_at=now,
        expires_at=now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(refresh_token_record)
    db.commit()

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/auth",
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "user_type": user.user_type.value,
        },
    }


@router.post("/refresh")
def refresh(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: Optional[str] = Cookie(default=None),
):
    if not refresh_token:
        raise api_error(401, "NOT_AUTHENTICATED", "Refresh token missing")

    token_hash = hash_refresh_token(refresh_token)
    now = datetime.now(timezone.utc)
    token_record = db.scalar(select(RefreshToken).where(RefreshToken.token_hash == token_hash))

    if not token_record or token_record.revoked_at or token_record.expires_at < now:
        raise api_error(401, "INVALID_REFRESH_TOKEN", "Refresh token is invalid or expired")

    user = db.get(User, token_record.user_id)
    access_token = create_access_token(user_id=user.id, user_type=user.user_type.value)

    # rotate refresh token
    token_record.revoked_at = now
    new_refresh_token = create_refresh_token()
    db.add(RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(new_refresh_token),
        created_at=now,
        expires_at=now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    ))
    db.commit()

    response.set_cookie("refresh_token", new_refresh_token, httponly=True, secure=True,
                         samesite="lax", max_age=REFRESH_TOKEN_EXPIRE_DAYS*24*60*60, path="/auth")

    return {"access_token": access_token, "token_type": "bearer"}