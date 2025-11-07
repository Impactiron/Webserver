"""Tests for database setup and models."""

import pytest
from sqlalchemy import inspect

from bestellsystem.db import Base, SessionLocal, engine, get_session
from bestellsystem.models import User


def test_engine_created():
    """Test that the database engine is created."""
    assert engine is not None
    assert engine.url is not None


def test_session_factory_created():
    """Test that the session factory is created."""
    assert SessionLocal is not None


def test_get_session():
    """Test that get_session returns a valid session."""
    session = get_session()
    assert session is not None
    session.close()


def test_base_metadata():
    """Test that Base has metadata."""
    assert Base.metadata is not None


def test_user_model_exists():
    """Test that User model exists."""
    assert User is not None


def test_user_model_tablename():
    """Test that User model has correct table name."""
    assert User.__tablename__ == "user"


def test_user_model_columns():
    """Test that User model has required columns."""
    # Create a temporary in-memory database for testing
    from sqlalchemy import create_engine
    
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(test_engine)
    
    inspector = inspect(test_engine)
    columns = inspector.get_columns("user")
    column_names = [col["name"] for col in columns]
    
    assert "id" in column_names
    assert "email" in column_names
    assert "password_hash" in column_names
    assert "role" in column_names
    assert "created_at" in column_names


def test_user_email_unique_constraint():
    """Test that User email has unique constraint."""
    from sqlalchemy import create_engine
    
    test_engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(test_engine)
    
    inspector = inspect(test_engine)
    unique_constraints = inspector.get_unique_constraints("user")
    
    # Check that there's a unique constraint on email
    email_unique = any(
        "email" in constraint.get("column_names", [])
        for constraint in unique_constraints
    )
    assert email_unique
