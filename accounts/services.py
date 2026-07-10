"""Business logic for authentication workflows."""
import logging

from django.db import transaction
from rest_framework_simplejwt.exceptions import TokenError

from accounts.signals import account_status_changed, password_changed, user_created
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


@transaction.atomic
def set_user_active_status(user, is_active: bool, *, changed_by=None) -> bool:
    """Set a user's active status and email them when an admin activates the account.

    Returns True when the active state changed.
    """
    was_active = user.is_active
    if was_active == is_active:
        return False
    user.is_active = is_active
    user.save(update_fields=["is_active", "updated_at"])
    logger.info(
        "User %s was %s by %s",
        user.email,
        "activated" if is_active else "deactivated",
        getattr(changed_by, "email", changed_by),
    )
    account_status_changed.send(sender=user.__class__, user=user, is_active=is_active, changed_by=changed_by)
    return True
