"""Consistent API response helpers."""
from typing import Any

from rest_framework.response import Response


def success_response(message: str, data: Any = None, status_code: int = 200) -> Response:
    return Response({"success": True, "message": message, "data": data}, status=status_code)


def error_response(message: str, errors: Any = None, status_code: int = 400) -> Response:
    return Response({"success": False, "message": message, "data": errors}, status=status_code)
