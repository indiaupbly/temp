"""Reusable helper utilities."""
import secrets
import string
from datetime import datetime

from django.utils import timezone
from django.utils.text import slugify

from common.constants import OTP_LENGTH, PASSWORD_LENGTH


def generate_random_password(length: int = PASSWORD_LENGTH) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_otp(length: int = OTP_LENGTH) -> str:
    return "".join(secrets.choice(string.digits) for _ in range(length))


def slugify_name(name: str) -> str:
    return slugify(name).replace("-", "_")


def generate_teacher_id(name: str) -> str:
    return f"TCH-{slugify_name(name).upper()}-{secrets.randbelow(9999):04d}"


def generate_student_id(name: str) -> str:
    return f"STD-{slugify_name(name).upper()}-{secrets.randbelow(9999):04d}"


def current_datetime() -> datetime:
    return timezone.now()
