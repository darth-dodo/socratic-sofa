"""
Structured logging configuration for Socratic Sofa.

Provides consistent, structured logging across the application with:
- JSON formatting for production
- Pretty console output for development
- Context-aware logging with request/session IDs
- Performance timing utilities
"""

import logging
import sys
import time
from contextlib import contextmanager
from functools import wraps
from typing import Any

# Configure base logging
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: int = LOG_LEVEL, json_output: bool = False) -> logging.Logger:
    """
    Configure and return the root logger for the application.

    Args:
        level: Logging level (default: INFO)
        json_output: If True, output JSON format (for production)

    Returns:
        Configured root logger
    """
    # Create formatter
    if json_output:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # Configure handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    # Configure root logger
    root_logger = logging.getLogger("socratic_sofa")
    root_logger.setLevel(level)
    root_logger.handlers = []  # Clear existing handlers
    root_logger.addHandler(handler)
    # Allow propagation for testing (caplog needs this)
    root_logger.propagate = True

    return root_logger


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured log output."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        import json
        from datetime import UTC, datetime

        log_data = {
            "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields if present
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


class LoggerAdapter(logging.LoggerAdapter):
    """
    Custom logger adapter that adds context to log messages.

    Usage:
        logger = get_logger(__name__)
        logger = logger.with_context(topic="justice", session_id="abc123")
        logger.info("Processing topic")  # Includes context
    """

    def process(self, msg: str, kwargs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """Add extra context to log message."""
        extra = kwargs.get("extra", {})
        extra.update(self.extra)
        kwargs["extra"] = extra
        return msg, kwargs

    def with_context(self, **context: Any) -> "LoggerAdapter":
        """Create a new adapter with additional context."""
        new_extra = {**self.extra, **context}
        return LoggerAdapter(self.logger, new_extra)


def get_logger(name: str, **context: Any) -> LoggerAdapter:
    """
    Get a logger with optional context.

    Args:
        name: Logger name (usually __name__)
        **context: Optional context to include in all log messages

    Returns:
        LoggerAdapter with context support
    """
    logger = logging.getLogger(f"socratic_sofa.{name}")
    return LoggerAdapter(logger, context)


@contextmanager
def log_timing(logger: LoggerAdapter, operation: str, **extra: Any):
    """
    Context manager to log timing of operations.

    Usage:
        with log_timing(logger, "crew_execution", topic="justice"):
            crew.kickoff()
    """
    start_time = time.perf_counter()
    logger.info(f"Starting {operation}", extra={"operation": operation, **extra})

    try:
        yield
    except Exception as e:
        elapsed = time.perf_counter() - start_time
        logger.error(
            f"Failed {operation} after {elapsed:.2f}s: {e}",
            extra={"operation": operation, "elapsed_seconds": elapsed, "error": str(e), **extra},
        )
        raise
    else:
        elapsed = time.perf_counter() - start_time
        logger.info(
            f"Completed {operation} in {elapsed:.2f}s",
            extra={"operation": operation, "elapsed_seconds": elapsed, **extra},
        )


def log_function_call(logger: LoggerAdapter | None = None):
    """
    Decorator to log function entry/exit with timing.

    Usage:
        @log_function_call()
        def my_function(arg1, arg2):
            ...
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_logger = logger or get_logger(func.__module__)
            func_name = func.__qualname__

            func_logger.debug(
                f"Entering {func_name}",
                extra={"function": func_name, "event": "function_entry"},
            )

            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start_time

                func_logger.debug(
                    f"Exiting {func_name} after {elapsed:.3f}s",
                    extra={
                        "function": func_name,
                        "event": "function_exit",
                        "elapsed_seconds": elapsed,
                    },
                )
                return result

            except Exception as e:
                elapsed = time.perf_counter() - start_time
                func_logger.error(
                    f"Exception in {func_name} after {elapsed:.3f}s: {e}",
                    extra={
                        "function": func_name,
                        "event": "function_error",
                        "elapsed_seconds": elapsed,
                        "error_type": type(e).__name__,
                    },
                )
                raise

        return wrapper

    return decorator


# Initialize logging on module import
_root_logger = setup_logging()
