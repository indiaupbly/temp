from pathlib import Path
from django.core.exceptions import ValidationError


def validate_school_logo(file_obj) -> None:
    if file_obj.size > 2 * 1024 * 1024:
        raise ValidationError("School logo must not exceed 2MB.")
    if Path(file_obj.name).suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise ValidationError("Only JPG, PNG, or WEBP images are allowed.")
