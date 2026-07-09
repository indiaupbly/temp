"""Custom exceptions and DRF exception handling."""
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class AIServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "AI service is currently unavailable."
    default_code = "ai_service_unavailable"


class CSVValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "CSV validation failed."
    default_code = "csv_validation_error"


class ImageValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Image validation failed."
    default_code = "image_validation_error"


class DuplicateRecord(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Duplicate record found."
    default_code = "duplicate_record"


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {"success": False, "message": str(exc.detail) if hasattr(exc, "detail") else str(exc), "data": response.data}
    return response
