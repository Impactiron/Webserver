"""Tests for the Flask application."""

import pytest

from bestellsystem.app import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_health_endpoint_json_content_type(client):
    """Test health endpoint returns JSON content type."""
    response = client.get("/api/v1/health")
    assert response.content_type == "application/json"
