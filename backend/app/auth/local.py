from __future__ import annotations

import hashlib
import hmac
import os
from datetime import UTC, datetime, timedelta
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from app.core.config import settings

security = HTTPBearer(auto_error=False)


class AuthenticatedUser(BaseModel):
    user_id: str
    email: str | None = None
    name: str | None = None
    is_admin: bool = False

    @property
    def clerk_user_id(self) -> str:
        # The DB column keeps its original name to avoid a risky migration.
        return self.user_id


class StoredUser(BaseModel):
    id: str
    email: str
    password_hash: str
    full_name: str | None = None
    is_admin: bool = False


class SignupRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=120)


class LoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=1, max_length=128)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthenticatedUser


_memory_users_by_email: dict[str, StoredUser] = {}


def signup_user(request: SignupRequest) -> AuthResponse:
    email = _normalize_email(request.email)
    if _find_user_by_email(email):
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    user = StoredUser(
        id=str(uuid4()),
        email=email,
        password_hash=hash_password(request.password),
        full_name=(request.full_name or "").strip() or None,
        is_admin=_is_admin_email(email),
    )
    _save_user(user)
    auth_user = AuthenticatedUser(user_id=user.id, email=user.email, name=user.full_name, is_admin=user.is_admin)
    return AuthResponse(access_token=create_access_token(auth_user), user=auth_user)


def login_user(request: LoginRequest) -> AuthResponse:
    user = _find_user_by_email(_normalize_email(request.email))
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    auth_user = AuthenticatedUser(user_id=user.id, email=user.email, name=user.full_name, is_admin=user.is_admin)
    return AuthResponse(access_token=create_access_token(auth_user), user=auth_user)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> AuthenticatedUser:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing bearer token.")

    if credentials.credentials == "dev-token" and settings.allow_dev_auth and not settings.is_production:
        return AuthenticatedUser(user_id="dev-user", email="dev@example.com", is_admin=True)

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid bearer token.") from exc

    user_id = str(payload.get("sub") or "")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid bearer token.")
    return AuthenticatedUser(user_id=user_id, email=payload.get("email"), name=payload.get("name"), is_admin=bool(payload.get("is_admin")))


def create_access_token(user: AuthenticatedUser) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": user.user_id,
        "email": user.email,
        "name": user.name,
        "is_admin": user.is_admin,
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    iterations = 390000
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations_text, salt_hex, digest_hex = stored_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations_text),
        )
        return hmac.compare_digest(digest.hex(), digest_hex)
    except Exception:
        return False


def _normalize_email(email: str) -> str:
    normalized = email.strip().lower()
    if "@" not in normalized or "." not in normalized.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Enter a valid email address.")
    return normalized


def _find_user_by_email(email: str) -> StoredUser | None:
    if settings.supabase_url and settings.supabase_service_role_key:
        from supabase import create_client

        client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        data = client.table("user_profiles").select("*").eq("email", email).execute().data
        if not data:
            return None
        row = data[0]
        password_hash = row.get("password_hash")
        if not password_hash:
            return None
        return StoredUser(
            id=str(row["id"]),
            email=row["email"],
            password_hash=password_hash,
            full_name=row.get("full_name"),
            is_admin=bool(row.get("is_admin")),
        )
    return _memory_users_by_email.get(email)


def _save_user(user: StoredUser) -> None:
    if settings.supabase_url and settings.supabase_service_role_key:
        from supabase import create_client

        client = create_client(settings.supabase_url, settings.supabase_service_role_key)
        client.table("user_profiles").insert(
            {
                "id": user.id,
                "clerk_user_id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "password_hash": user.password_hash,
                "auth_provider": "local",
                "is_admin": user.is_admin,
            }
        ).execute()
        return
    _memory_users_by_email[user.email] = user


def _is_admin_email(email: str) -> bool:
    return email.lower() in settings.admin_email_set


def require_admin(user: Annotated[AuthenticatedUser, Depends(get_current_user)]) -> AuthenticatedUser:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required.")
    return user
