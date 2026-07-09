"""Reusable helper utilities."""
import secrets
import string
from datetime import datetime

from django.utils import timezone

from common.constants import PASSWORD_LENGTH


def generate_random_password(length: int = PASSWORD_LENGTH) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def current_datetime() -> datetime:
    return timezone.now()
