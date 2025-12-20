# Logging Config API Reference

## Overview

The `logging_config.py` module provides structured logging infrastructure for Socratic Sofa with context-aware logging, performance tracking, and JSON output support for production environments.

**Key Features**:
- **Structured Logging**: Consistent log format with contextual metadata
- **JSON Output**: Machine-parsable logs for production monitoring
- **Performance Tracking**: Automatic timing utilities for operations
- **Context Propagation**: Session IDs, topics, and request metadata
- **Function Decorators**: Automatic entry/exit logging with timing

---

## Functions

### `setup_logging()`

Configure and return the root logger for the application.

**Signature**:

```python
def setup_logging(level: int = LOG_LEVEL, json_output: bool = False) -> logging.Logger
```

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `level` | `int` | `LOG_LEVEL` (INFO) | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `json_output` | `bool` | `False` | If True, output JSON format for production |

**Returns**: `logging.Logger` - Configured root logger instance

**Example**:

```python
from socratic_sofa.logging_config import setup_logging
import logging

# Development: Human-readable console output
logger = setup_logging(level=logging.DEBUG, json_output=False)

# Production: JSON format for log aggregation
logger = setup_logging(level=logging.INFO, json_output=True)
```

**Console Format** (Development):

```
2024-12-20 17:30:45 | INFO     | socratic_sofa.content_filter | Topic approved
```

**JSON Format** (Production):

```json
{
  "timestamp": "2024-12-20T17:30:45.123Z",
  "level": "INFO",
  "logger": "socratic_sofa.content_filter",
  "message": "Topic approved",
  "topic": "What is justice?"
}
```

---

### `get_logger()`

Get a logger with optional context for structured logging.

**Signature**:

```python
def get_logger(name: str, **context: Any) -> LoggerAdapter
```

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Logger name (usually `__name__`) |
| `**context` | `Any` | Optional context to include in all log messages |

**Returns**: `LoggerAdapter` - Logger with context support

**Example**:

```python
from socratic_sofa.logging_config import get_logger

# Basic logger
logger = get_logger(__name__)
logger.info("Processing request")

# Logger with context
logger = get_logger(__name__, session_id="abc123", user="guest")
logger.info("Topic selected")
# Logs: {..., "session_id": "abc123", "user": "guest", ...}

# Add more context later
logger = logger.with_context(topic="justice")
logger.info("Moderation started")
# Logs: {..., "session_id": "abc123", "user": "guest", "topic": "justice", ...}
```

**Context Chaining**:

```python
# Start with base context
logger = get_logger(__name__, module="content_filter")

# Add session context
session_logger = logger.with_context(session_id="xyz789")

# Add request context
request_logger = session_logger.with_context(
    topic="What is truth?",
    user_agent="Mozilla/5.0"
)

# All logs include accumulated context
request_logger.info("Request processed")
```

---

### `log_timing()`

Context manager to log timing of operations with automatic error handling.

**Signature**:

```python
@contextmanager
def log_timing(logger: LoggerAdapter, operation: str, **extra: Any)
```

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `logger` | `LoggerAdapter` | Logger instance to use |
| `operation` | `str` | Name of the operation being timed |
| `**extra` | `Any` | Additional context to include in logs |

**Example**:

```python
from socratic_sofa.logging_config import get_logger, log_timing

logger = get_logger(__name__)

# Time an operation
with log_timing(logger, "crew_execution", topic="justice"):
    crew = SocraticSofa().crew()
    result = crew.kickoff(inputs=inputs)

# Logs on entry:
# INFO | Starting crew_execution | {"operation": "crew_execution", "topic": "justice"}

# Logs on success:
# INFO | Completed crew_execution in 127.45s | {..., "elapsed_seconds": 127.45}

# Logs on error:
# ERROR | Failed crew_execution after 45.23s: API timeout | {..., "elapsed_seconds": 45.23, "error": "API timeout"}
```

**Nested Timing**:

```python
with log_timing(logger, "dialogue_generation", topic="justice"):
    with log_timing(logger, "content_moderation"):
        is_appropriate = moderate_topic(topic)

    with log_timing(logger, "crew_execution"):
        result = crew.kickoff(inputs)

    with log_timing(logger, "output_formatting"):
        outputs = format_results(result)
```

---

### `log_function_call()`

Decorator to log function entry/exit with automatic timing.

**Signature**:

```python
def log_function_call(logger: LoggerAdapter | None = None)
```

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `logger` | `LoggerAdapter \| None` | `None` | Logger to use (auto-creates if None) |

**Returns**: Decorator function

**Example**:

```python
from socratic_sofa.logging_config import get_logger, log_function_call

logger = get_logger(__name__)

@log_function_call(logger)
def process_topic(topic: str) -> dict:
    """Process a philosophical topic."""
    # Function logic...
    return {"result": "processed"}

# Logs on entry:
# DEBUG | Entering process_topic | {"function": "process_topic", "event": "function_entry"}

# Logs on exit:
# DEBUG | Exiting process_topic after 2.345s | {..., "event": "function_exit", "elapsed_seconds": 2.345}

# Logs on error:
# ERROR | Exception in process_topic after 1.234s: ValueError | {..., "error_type": "ValueError"}
```

**Class Methods**:

```python
class ContentFilter:
    def __init__(self):
        self.logger = get_logger(__name__)

    @log_function_call()  # Auto-creates logger from module
    def is_appropriate(self, topic: str) -> bool:
        # Function logic...
        return True

    @log_function_call(logger)  # Uses instance logger
    def get_suggestions(self) -> list[str]:
        # Function logic...
        return ["topic1", "topic2"]
```

---

## Classes

### `JsonFormatter`

JSON formatter for structured log output in production environments.

**Usage**:

```python
import logging
from socratic_sofa.logging_config import JsonFormatter

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger = logging.getLogger("socratic_sofa")
logger.addHandler(handler)

logger.info("Processing request", extra={"user_id": "123"})
```

**Output**:

```json
{
  "timestamp": "2024-12-20T17:30:45.123456Z",
  "level": "INFO",
  "logger": "socratic_sofa",
  "message": "Processing request",
  "user_id": "123"
}
```

**Exception Handling**:

```python
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed", exc_info=True)
```

**Output with Exception**:

```json
{
  "timestamp": "2024-12-20T17:30:45.123456Z",
  "level": "ERROR",
  "logger": "socratic_sofa",
  "message": "Operation failed",
  "exception": "Traceback (most recent call last):\n  File ..."
}
```

---

### `LoggerAdapter`

Custom logger adapter that adds context to log messages with chaining support.

**Methods**:

#### `process()`

Add extra context to log message before emission.

**Signature**:

```python
def process(self, msg: str, kwargs: dict[str, Any]) -> tuple[str, dict[str, Any]]
```

#### `with_context()`

Create a new adapter with additional context (non-mutating).

**Signature**:

```python
def with_context(self, **context: Any) -> "LoggerAdapter"
```

**Example**:

```python
# Base logger
logger = get_logger(__name__, service="api")

# Request logger (includes service context)
request_logger = logger.with_context(request_id="req_123")
request_logger.info("Request started")  # Has service + request_id

# Session logger (includes service + request context)
session_logger = request_logger.with_context(session_id="sess_456")
session_logger.info("Processing")  # Has all three contexts

# Original logger unchanged
logger.info("New request")  # Only has service context
```

---

## Constants

### `LOG_LEVEL`

Default logging level: `logging.INFO`

### `LOG_FORMAT`

Console log format string:
```
"%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
```

### `DATE_FORMAT`

Date format for console logs:
```
"%Y-%m-%d %H:%M:%S"
```

---

## Complete Integration Example

```python
from socratic_sofa.logging_config import (
    setup_logging,
    get_logger,
    log_timing,
    log_function_call
)

# Initialize logging (usually in main.py)
setup_logging(level=logging.INFO, json_output=False)

# Module-level logger
logger = get_logger(__name__, module="content_filter")

# Function with automatic logging
@log_function_call(logger)
def moderate_content(topic: str) -> tuple[bool, str]:
    """Moderate a topic for appropriateness."""

    # Add context for this request
    request_logger = logger.with_context(
        topic=topic[:50],
        topic_length=len(topic)
    )

    # Time a critical operation
    with log_timing(request_logger, "api_call"):
        result = call_moderation_api(topic)

    request_logger.info("Moderation complete", extra={"result": result})
    return result

# Usage
is_ok, reason = moderate_content("What is justice?")
```

**Console Output**:

```
2024-12-20 17:30:45 | DEBUG    | socratic_sofa.content_filter | Entering moderate_content
2024-12-20 17:30:45 | INFO     | socratic_sofa.content_filter | Starting api_call
2024-12-20 17:30:46 | INFO     | socratic_sofa.content_filter | Completed api_call in 0.85s
2024-12-20 17:30:46 | INFO     | socratic_sofa.content_filter | Moderation complete
2024-12-20 17:30:46 | DEBUG    | socratic_sofa.content_filter | Exiting moderate_content after 1.02s
```

---

## Best Practices

### 1. Use Structured Context

```python
# ✅ Good: Structured context
logger.info("Topic moderated", extra={
    "topic": topic[:50],
    "result": "approved",
    "duration_ms": 850
})

# ❌ Bad: String formatting
logger.info(f"Topic '{topic}' was approved in 850ms")
```

### 2. Chain Context Appropriately

```python
# ✅ Good: Progressive context building
base_logger = get_logger(__name__)
session_logger = base_logger.with_context(session_id=session_id)
request_logger = session_logger.with_context(request_id=request_id)

# ❌ Bad: Recreating logger each time
logger = get_logger(__name__, session_id=session_id, request_id=request_id)
```

### 3. Use Appropriate Log Levels

```python
# DEBUG: Detailed diagnostic information
logger.debug("Function called", extra={"args": args})

# INFO: Confirmation of normal operation
logger.info("Request processed successfully")

# WARNING: Unexpected but recoverable issues
logger.warning("Rate limit approaching", extra={"calls_remaining": 2})

# ERROR: Failures requiring attention
logger.error("API call failed", extra={"error": str(e)}, exc_info=True)
```

### 4. Time Critical Operations

```python
# ✅ Good: Time important operations
with log_timing(logger, "database_query", table="topics"):
    results = db.query(...)

# ❌ Bad: Manual timing
start = time.time()
results = db.query(...)
logger.info(f"Query took {time.time() - start}s")
```

---

## Notes

- Logger is automatically initialized on module import
- Use `setup_logging()` early in application startup
- JSON output recommended for production environments
- Context is immutable - `with_context()` creates new adapter
- All timing includes microsecond precision
- Exception info automatically formatted in JSON output
- Log propagation enabled for pytest `caplog` compatibility
