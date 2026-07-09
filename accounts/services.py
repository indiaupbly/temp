"""Business logic for authentication workflows."""
import logging

from django.conf import settings
from django.db import transaction
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)


def _tokens_for_user(user) -> dict[str, str]:
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


@transaction.atomic
def login_user(user) -> dict[str, object]:
    logger.info("User logged in: %s", user.email)
    return {"user": user, "tokens": _tokens_for_user(user)}


def logout_user(refresh_token: str | None) -> None:
    if not refresh_token:
        return
    try:
        RefreshToken(refresh_token).blacklist()
    except TokenError:
        logger.warning("Attempted logout with invalid refresh token.")


def refresh_user_tokens(refresh_token: str | None) -> dict[str, str]:
    if not refresh_token:
        raise TokenError("Refresh token cookie is missing.")
    refresh = RefreshToken(refresh_token)
    access_token = str(refresh.access_token)
    tokens = {"access": access_token, "refresh": str(refresh)}
    if settings.SIMPLE_JWT.get("ROTATE_REFRESH_TOKENS"):
        if settings.SIMPLE_JWT.get("BLACKLIST_AFTER_ROTATION"):
            refresh.blacklist()
        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()
        tokens["refresh"] = str(refresh)
    return tokens
