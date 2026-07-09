"""Shared validators."""
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator

from common.constants import PASSWORD_LENGTH, PHONE_LENGTH

validate_email = EmailValidator(message="Enter a valid email address.")
validate_phone = RegexValidator(regex=rf"^\d{{{PHONE_LENGTH}}}$", message="Enter a valid 10-digit phone number.")


def validate_password_strength(password: str) -> None:
    if len(password) < PASSWORD_LENGTH:
        raise ValidationError(f"Password must be at least {PASSWORD_LENGTH} characters long.")
    if password.isdigit() or password.isalpha():
        raise ValidationError("Password must contain a mix of letters, numbers, or symbols.")


def validate_csv_file(file_obj) -> None:
    if Path(file_obj.name).suffix.lower() != ".csv":
        raise ValidationError("Only CSV files are allowed.")


def validate_image_file(file_obj) -> None:
    allowed = {".jpg", ".jpeg", ".png", ".webp"}
    if Path(file_obj.name).suffix.lower() not in allowed:
        raise ValidationError("Only JPG, PNG, or WEBP image files are allowed.")
