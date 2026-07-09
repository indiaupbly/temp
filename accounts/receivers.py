"""Signal receivers for account side effects."""
import logging

from django.dispatch import receiver

from accounts.signals import password_changed, user_created
from common.emails import send_html_email

logger = logging.getLogger(__name__)


@receiver(user_created)
def send_account_created_email(sender, user, raw_password=None, **kwargs):
    try:
        send_html_email(
            "Your account has been created",
            "emails/account_created.html",
            {"user": user, "password": raw_password},
            [user.email],
        )
    except Exception:
        logger.exception("Failed to send account created email to %s", user.email)


@receiver(password_changed)
def send_password_changed_email(sender, user, changed_by=None, **kwargs):
    try:
        send_html_email(
            "Your password has been changed",
            "emails/password_changed.html",
            {"user": user, "changed_by": changed_by},
            [user.email],
        )
    except Exception:
        logger.exception("Failed to send password changed email to %s", user.email)
