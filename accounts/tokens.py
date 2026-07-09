"""JWT token helpers for account authentication."""
from typing import Any

from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken


def generate_refresh(user) -> str:
    """Generate a refresh token for a user."""
    return str(RefreshToken.for_user(user))


def generate_access(user=None, refresh_token: str | RefreshToken | None = None) -> str:
    """Generate an access token from a user or an existing refresh token."""
    if refresh_token is not None:
        refresh = refresh_token if isinstance(refresh_token, RefreshToken) else RefreshToken(refresh_token)
        return str(refresh.access_token)
    if user is None:
        raise ValueError("A user or refresh_token is required to generate an access token.")
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def generate_pair(user) -> dict[str, str]:
    """Generate an access/refresh token pair for a user."""
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


def verify(token: str):
    """Validate any supported JWT token and return the validated token object."""
    return UntypedToken(token)


def decode(token: str) -> dict[str, Any]:
    """Decode a token after verifying its signature, expiry, and blacklist state."""
    return dict(verify(token).payload)


def blacklist(refresh_token: str | RefreshToken | None) -> None:
    """Blacklist a refresh token when token blacklist support is enabled."""
    if not refresh_token:
        return
    token = refresh_token if isinstance(refresh_token, RefreshToken) else RefreshToken(refresh_token)
    token.blacklist()


def rotate_refresh(refresh_token: str) -> dict[str, str]:
    """Refresh an access token and optionally rotate the refresh token."""
    refresh = RefreshToken(refresh_token)
    tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}
    if settings.SIMPLE_JWT.get("ROTATE_REFRESH_TOKENS"):
        if settings.SIMPLE_JWT.get("BLACKLIST_AFTER_ROTATION"):
            refresh.blacklist()
        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()
        tokens["refresh"] = str(refresh)
    return tokens
