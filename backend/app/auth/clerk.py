from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient
from pydantic import BaseModel

from app.core.config import settings

security = HTTPBearer(auto_error=False)


class AuthenticatedUser(BaseModel):
    clerk_user_id: str
    email: str | None = None
    name: str | None = None


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> AuthenticatedUser:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing bearer token.")

    if (
        credentials.credentials == "dev-token"
        and settings.allow_dev_auth
        and not settings.is_production
    ):
        return AuthenticatedUser(clerk_user_id="dev-user", email="dev@example.com")

    if not settings.clerk_jwks_url:
        raise HTTPException(status_code=500, detail="Clerk JWKS URL is not configured.")

    try:
        jwks_client = PyJWKClient(settings.clerk_jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(credentials.credentials)
        payload = jwt.decode(
            credentials.credentials,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid bearer token.") from exc

    return AuthenticatedUser(
        clerk_user_id=str(payload.get("sub")),
        email=payload.get("email"),
        name=payload.get("name"),
    )
