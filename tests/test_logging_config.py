"""
Unit tests for logging_config module.
Tests structured logging configuration and utilities.
"""

import logging
import time
from unittest.mock import Mock

import pytest

from socratic_sofa.logging_config import (
    JsonFormatter,
    LoggerAdapter,
    get_logger,
    log_function_call,
    log_timing,
    setup_logging,
)


class TestSetupLogging:
    """Test suite for setup_logging function."""

    def test_returns_logger_instance(self):
        """Test that setup_logging returns a logger."""
        logger = setup_logging()
        assert isinstance(logger, logging.Logger)

    def test_logger_name_is_socratic_sofa(self):
        """Test that logger has correct name."""
        logger = setup_logging()
        assert logger.name == "socratic_sofa"

    def test_default_level_is_info(self):
        """Test that default log level is INFO."""
        logger = setup_logging()
        assert logger.level == logging.INFO

    def test_custom_level_is_applied(self):
        """Test that custom log level is applied."""
        logger = setup_logging(level=logging.DEBUG)
        assert logger.level == logging.DEBUG

    def test_has_handler(self):
        """Test that logger has at least one handler."""
        logger = setup_logging()
        assert len(logger.handlers) >= 1

    def test_json_output_uses_json_formatter(self):
        """Test that json_output=True uses JsonFormatter."""
        logger = setup_logging(json_output=True)
        handler = logger.handlers[0]
        assert isinstance(handler.formatter, JsonFormatter)


class TestJsonFormatter:
    """Test suite for JsonFormatter class."""

    def test_format_returns_valid_json(self):
        """Test that format returns valid JSON string."""
        import json

        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)
        parsed = json.loads(result)

        assert isinstance(parsed, dict)

    def test_format_includes_timestamp(self):
        """Test that formatted output includes timestamp."""
        import json

        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)
        parsed = json.loads(result)

        assert "timestamp" in parsed
        assert parsed["timestamp"].endswith("Z")

    def test_format_includes_level(self):
        """Test that formatted output includes log level."""
        import json

        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname="test.py",
            lineno=10,
            msg="Warning message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)
        parsed = json.loads(result)

        assert parsed["level"] == "WARNING"

    def test_format_includes_message(self):
        """Test that formatted output includes message."""
        import json

        formatter = JsonFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="My test message",
            args=(),
            exc_info=None,
        )

        result = formatter.format(record)
        parsed = json.loads(result)

        assert parsed["message"] == "My test message"


class TestLoggerAdapter:
    """Test suite for LoggerAdapter class."""

    def test_with_context_returns_new_adapter(self):
        """Test that with_context returns a new LoggerAdapter."""
        base_logger = logging.getLogger("test")
        adapter = LoggerAdapter(base_logger, {"key": "value"})

        new_adapter = adapter.with_context(new_key="new_value")

        assert isinstance(new_adapter, LoggerAdapter)
        assert new_adapter is not adapter

    def test_with_context_preserves_existing_context(self):
        """Test that with_context preserves existing context."""
        base_logger = logging.getLogger("test")
        adapter = LoggerAdapter(base_logger, {"key1": "value1"})

        new_adapter = adapter.with_context(key2="value2")

        assert new_adapter.extra["key1"] == "value1"
        assert new_adapter.extra["key2"] == "value2"

    def test_with_context_allows_override(self):
        """Test that with_context allows overriding existing keys."""
        base_logger = logging.getLogger("test")
        adapter = LoggerAdapter(base_logger, {"key": "old_value"})

        new_adapter = adapter.with_context(key="new_value")

        assert new_adapter.extra["key"] == "new_value"


class TestGetLogger:
    """Test suite for get_logger function."""

    def test_returns_logger_adapter(self):
        """Test that get_logger returns a LoggerAdapter."""
        logger = get_logger("test_module")
        assert isinstance(logger, LoggerAdapter)

    def test_logger_name_includes_module(self):
        """Test that logger name includes the module name."""
        logger = get_logger("my_module")
        assert "my_module" in logger.logger.name

    def test_accepts_initial_context(self):
        """Test that get_logger accepts initial context."""
        logger = get_logger("test", request_id="123", user="test_user")

        assert logger.extra["request_id"] == "123"
        assert logger.extra["user"] == "test_user"


class TestLogTiming:
    """Test suite for log_timing context manager."""

    def test_logs_start_message(self, caplog):
        """Test that log_timing logs start message."""
        logger = get_logger("test")

        with caplog.at_level(logging.INFO, logger="socratic_sofa"):
            with log_timing(logger, "test_operation"):
                pass

        assert any("Starting test_operation" in record.message for record in caplog.records)

    def test_logs_completion_message(self, caplog):
        """Test that log_timing logs completion message."""
        logger = get_logger("test")

        with caplog.at_level(logging.INFO, logger="socratic_sofa"):
            with log_timing(logger, "test_operation"):
                pass

        assert any("Completed test_operation" in record.message for record in caplog.records)

    def test_logs_failure_on_exception(self, caplog):
        """Test that log_timing logs failure on exception."""
        logger = get_logger("test")

        with caplog.at_level(logging.ERROR, logger="socratic_sofa"):
            with pytest.raises(ValueError):
                with log_timing(logger, "failing_operation"):
                    raise ValueError("Test error")

        assert any("Failed failing_operation" in record.message for record in caplog.records)

    def test_includes_elapsed_time(self, caplog):
        """Test that log_timing includes elapsed time."""
        logger = get_logger("test")

        with caplog.at_level(logging.INFO, logger="socratic_sofa"):
            with log_timing(logger, "timed_operation"):
                time.sleep(0.1)

        # Check that completion message includes timing
        completion_records = [r for r in caplog.records if "Completed" in r.message]
        assert len(completion_records) == 1
        assert "0.1" in completion_records[0].message or "0.2" in completion_records[0].message


class TestLogFunctionCall:
    """Test suite for log_function_call decorator."""

    def test_logs_function_entry(self, caplog):
        """Test that decorator logs function entry."""

        @log_function_call()
        def test_func():
            return "result"

        with caplog.at_level(logging.DEBUG, logger="socratic_sofa"):
            test_func()

        assert any("Entering" in record.message for record in caplog.records)

    def test_logs_function_exit(self, caplog):
        """Test that decorator logs function exit."""

        @log_function_call()
        def test_func():
            return "result"

        with caplog.at_level(logging.DEBUG, logger="socratic_sofa"):
            test_func()

        assert any("Exiting" in record.message for record in caplog.records)

    def test_logs_exception(self, caplog):
        """Test that decorator logs exceptions."""

        @log_function_call()
        def failing_func():
            raise ValueError("Test error")

        with caplog.at_level(logging.ERROR, logger="socratic_sofa"):
            with pytest.raises(ValueError):
                failing_func()

        assert any("Exception" in record.message for record in caplog.records)

    def test_preserves_return_value(self):
        """Test that decorator preserves function return value."""

        @log_function_call()
        def test_func():
            return "expected_result"

        result = test_func()
        assert result == "expected_result"

    def test_preserves_exceptions(self):
        """Test that decorator re-raises exceptions."""

        @log_function_call()
        def failing_func():
            raise ValueError("Expected error")

        with pytest.raises(ValueError, match="Expected error"):
            failing_func()
