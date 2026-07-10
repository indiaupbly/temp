"""Consistent API response helpers."""
from typing import Any

from rest_framework import status
from rest_framework.response import Response


def success_response(message: str, data: Any = None, status_code: int = status.HTTP_200_OK) -> Response:
    return Response({"success": True, "message": message, "data": data}, status=status_code)


def error_response(message: str, errors: Any = None, status_code: int = status.HTTP_400_BAD_REQUEST) -> Response:
    return Response({"success": False, "message": message, "errors": errors}, status=status_code)


def created_response(message: str = "Created successfully.", data: Any = None) -> Response:
    return success_response(message, data, status.HTTP_201_CREATED)


def updated_response(message: str = "Updated successfully.", data: Any = None) -> Response:
    return success_response(message, data, status.HTTP_200_OK)


def deleted_response(message: str = "Deleted successfully.", data: Any = None) -> Response:
    return success_response(message, data, status.HTTP_200_OK)


def no_content_response() -> Response:
    return Response(status=status.HTTP_204_NO_CONTENT)


def paginated_response(message: str = "Fetched successfully.", *, results: Any, count: int, next_url: str | None = None, previous_url: str | None = None) -> Response:
    return success_response(
        message,
        {"count": count, "next": next_url, "previous": previous_url, "results": results},
        status.HTTP_200_OK,
    )
