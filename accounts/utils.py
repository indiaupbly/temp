"""Account utilities."""
from django.conf import settings


def set_token_cookie(response, key: str, value: str, max_age: int | None = None) -> None:
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        secure=settings.JWT_COOKIE_SECURE,
        httponly=settings.JWT_COOKIE_HTTP_ONLY,
        samesite=settings.JWT_COOKIE_SAMESITE,
        path=settings.JWT_COOKIE_PATH,
    )


def delete_token_cookie(response, key: str) -> None:
    response.delete_cookie(key=key, path=settings.JWT_COOKIE_PATH, samesite=settings.JWT_COOKIE_SAMESITE)
