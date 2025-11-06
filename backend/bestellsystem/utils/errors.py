"""Unified error handling and response envelope."""

from typing import Any

from flask import jsonify
from werkzeug.exceptions import HTTPException


class APIError(Exception):
    """Base API error class."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Initialize API error.

        Args:
            message: Error message
            status_code: HTTP status code
            payload: Additional error details
        """
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary."""
        error_dict: dict[str, Any] = {
            "error": {
                "message": self.message,
                "status_code": self.status_code,
            }
        }
        if self.payload:
            error_dict["error"]["details"] = self.payload
        return error_dict


class ValidationError(APIError):
    """Validation error (400)."""

    def __init__(self, message: str, payload: dict[str, Any] | None = None) -> None:
        """Initialize validation error."""
        super().__init__(message, status_code=400, payload=payload)


class NotFoundError(APIError):
    """Not found error (404)."""

    def __init__(self, message: str, payload: dict[str, Any] | None = None) -> None:
        """Initialize not found error."""
        super().__init__(message, status_code=404, payload=payload)


class UnauthorizedError(APIError):
    """Unauthorized error (401)."""

    def __init__(self, message: str, payload: dict[str, Any] | None = None) -> None:
        """Initialize unauthorized error."""
        super().__init__(message, status_code=401, payload=payload)


class ForbiddenError(APIError):
    """Forbidden error (403)."""

    def __init__(self, message: str, payload: dict[str, Any] | None = None) -> None:
        """Initialize forbidden error."""
        super().__init__(message, status_code=403, payload=payload)


class InternalServerError(APIError):
    """Internal server error (500)."""

    def __init__(self, message: str, payload: dict[str, Any] | None = None) -> None:
        """Initialize internal server error."""
        super().__init__(message, status_code=500, payload=payload)


def handle_api_error(error: APIError) -> tuple[Any, int]:
    """Handle API errors and return JSON response.

    Args:
        error: API error instance

    Returns:
        Tuple of (JSON response, status code)
    """
    response = jsonify(error.to_dict())
    return response, error.status_code


def handle_http_exception(error: HTTPException) -> tuple[Any, int]:
    """Handle HTTP exceptions and return JSON response.

    Args:
        error: HTTP exception

    Returns:
        Tuple of (JSON response, status code)
    """
    response = jsonify(
        {
            "error": {
                "message": error.description or "An error occurred",
                "status_code": error.code or 500,
            }
        }
    )
    return response, error.code or 500


def handle_generic_exception(error: Exception) -> tuple[Any, int]:
    """Handle generic exceptions and return JSON response.

    Args:
        error: Generic exception

    Returns:
        Tuple of (JSON response, status code)
    """
    response = jsonify(
        {
            "error": {
                "message": "Internal server error",
                "status_code": 500,
            }
        }
    )
    return response, 500


def register_error_handlers(app: Any) -> None:
    """Register error handlers with Flask app.

    Args:
        app: Flask application instance
    """
    app.register_error_handler(APIError, handle_api_error)
    app.register_error_handler(HTTPException, handle_http_exception)
    app.register_error_handler(Exception, handle_generic_exception)
