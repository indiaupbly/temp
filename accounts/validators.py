"""Account-specific validators."""
from django.core.exceptions import ValidationError

from accounts.models import UserRole


def validate_role(role: str) -> None:
    if role not in UserRole.values:
        raise ValidationError("Invalid user role.")
