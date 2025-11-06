"""Tests for logging utilities."""

import json
import logging

from bestellsystem.utils.logging import JsonFormatter, get_logger, setup_logging


def test_json_formatter_format():
    """Test JSON formatter produces valid JSON."""
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    formatted = formatter.format(record)
    data = json.loads(formatted)

    assert "timestamp" in data
    assert data["level"] == "INFO"
    assert data["logger"] == "test"
    assert data["message"] == "Test message"


def test_get_logger():
    """Test get_logger returns logger instance."""
    logger = get_logger(__name__)
    assert isinstance(logger, logging.Logger)
    assert logger.name == __name__


def test_setup_logging_json():
    """Test setup_logging with JSON format."""
    setup_logging(level="INFO", log_format="json")
    root_logger = logging.getLogger()
    assert root_logger.level == logging.INFO
    assert len(root_logger.handlers) > 0


def test_setup_logging_text():
    """Test setup_logging with text format."""
    setup_logging(level="DEBUG", log_format="text")
    root_logger = logging.getLogger()
    assert root_logger.level == logging.DEBUG
