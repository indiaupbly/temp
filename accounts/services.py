"""Business logic for authentication workflows."""
import logging

from django.db import transaction
from rest_framework_simplejwt.exceptions import TokenError

from accounts.signals import password_changed
from accounts.tokens import blacklist, generate_pair, rotate_refresh

logger = logging.getLogger(__name__)


@transaction.atomic
def login_user(user) -> dict[str, object]:
    logger.info("User logged in: %s", user.email)
    return {"user": user, "tokens": generate_pair(user)}


def logout_user(refresh_token: str | None) -> None:
    try:
        blacklist(refresh_token)
    except TokenError:
        logger.warning("Attempted logout with invalid refresh token.")


def refresh_user_tokens(refresh_token: str | None) -> dict[str, str]:
    if not refresh_token:
        raise TokenError("Refresh token cookie is missing.")
    return rotate_refresh(refresh_token)


@transaction.atomic
def change_user_password(user, new_password: str, *, changed_by=None) -> None:
    user.set_password(new_password)
    user.save(update_fields=["password", "updated_at"])
    password_changed.send(sender=user.__class__, user=user, changed_by=changed_by)
