from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from sentry_sdk import capture_exception

import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    capture_exception(exc)
    # 1. Call DRF's default handler first
    response = exception_handler(exc, context)

    if response is not None:
        # 2. Extract error message (safe for frontend)
        error_message = (
            response.data.get("non_field_errors")  # Serializer errors
            or response.data.get("detail")  # APIException
            or "Invalid request"  # Fallback
        )

        # Handle lists (e.g., ["Error 1", "Error 2"])
        if isinstance(error_message, list):
            error_message = error_message[0]

        # 3. Standardized error response
        error_data = {
            "error": {
                "code": response.status_code,
                "message": str(error_message),
                "details": response.data
                if isinstance(response.data, dict)
                else str(response.data),
            },
            "status_code": response.status_code,
        }

        # 4. (Optional) Logging (avoid sensitive data!)
        request = context.get("request")
        logger.error(
            f"API Exception: {error_message}",
            exc_info=exc,
            extra={
                "path": request.path if request else None,
                "method": request.method if request else None,
                "status_code": response.status_code,
            },
        )

        return Response(error_data, status=response.status_code)

    # 5. Handle non-DRF exceptions (e.g., DatabaseError)
    logger.error("Unhandled Exception", exc_info=exc)
    return Response(
        {
            "error": {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Internal server error",
                "details": {},
            },
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
