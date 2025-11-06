"""Tests for error handling utilities."""

from bestellsystem.utils.errors import (
    APIError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)


def test_api_error_basic():
    """Test basic APIError."""
    error = APIError("Test error", status_code=400)
    assert error.message == "Test error"
    assert error.status_code == 400
    assert error.payload is None


def test_api_error_with_payload():
    """Test APIError with payload."""
    payload = {"field": "value"}
    error = APIError("Test error", status_code=400, payload=payload)
    error_dict = error.to_dict()

    assert error_dict["error"]["message"] == "Test error"
    assert error_dict["error"]["status_code"] == 400
    assert error_dict["error"]["details"] == payload


def test_validation_error():
    """Test ValidationError."""
    error = ValidationError("Invalid input")
    assert error.message == "Invalid input"
    assert error.status_code == 400


def test_not_found_error():
    """Test NotFoundError."""
    error = NotFoundError("Resource not found")
    assert error.message == "Resource not found"
    assert error.status_code == 404


def test_unauthorized_error():
    """Test UnauthorizedError."""
    error = UnauthorizedError("Authentication required")
    assert error.message == "Authentication required"
    assert error.status_code == 401


def test_forbidden_error():
    """Test ForbiddenError."""
    error = ForbiddenError("Access denied")
    assert error.message == "Access denied"
    assert error.status_code == 403


def test_internal_server_error():
    """Test InternalServerError."""
    error = InternalServerError("Server error")
    assert error.message == "Server error"
    assert error.status_code == 500
