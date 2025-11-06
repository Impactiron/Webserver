"""Tests for configuration module."""

import os

from bestellsystem.config import Config, DevelopmentConfig, ProductionConfig, get_config


def test_config_defaults():
    """Test default configuration values."""
    assert Config.HOST == "0.0.0.0"
    assert Config.PORT == 8000
    assert Config.LOG_LEVEL == "INFO"
    assert Config.LOG_FORMAT == "json"


def test_config_get():
    """Test configuration get method."""
    assert Config.get("HOST") == "0.0.0.0"
    assert Config.get("PORT") == 8000
    assert Config.get("NONEXISTENT", "default") == "default"


def test_get_config_development():
    """Test get_config returns development config by default."""
    os.environ["FLASK_ENV"] = "development"
    config = get_config()
    assert config == DevelopmentConfig
    assert config.DEBUG is True


def test_get_config_production():
    """Test get_config returns production config."""
    os.environ["FLASK_ENV"] = "production"
    config = get_config()
    assert config == ProductionConfig
    assert config.DEBUG is False
