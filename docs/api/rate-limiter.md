# Rate Limiter API Reference

## Overview

The `rate_limiter.py` module provides API call throttling for Socratic Sofa to prevent excessive requests to external services like the Anthropic content moderation endpoint.

**Key Features**:

- **Automatic Retry**: Sleep and retry on rate limit with exponential backoff
- **Fail Fast Option**: Immediately raise exception on rate limit
- **Structured Logging**: Integration with `logging_config` for tracking
- **Flexible Configuration**: Customizable call limits and time periods
- **Type Safety**: Full type hints for decorator usage

**Library**: Uses `ratelimit>=2.2.1` for implementation

---

## Functions

### `rate_limited()`

Decorator that applies rate limiting with automatic retry on limit exceeded.

**Signature**:

```python
def rate_limited(calls: int = DEFAULT_CALLS, period: int = DEFAULT_PERIOD) -> Callable[[F], F]
```

**Parameters**:

| Parameter | Type  | Default | Description                                   |
| --------- | ----- | ------- | --------------------------------------------- |
| `calls`   | `int` | `10`    | Maximum number of calls allowed in the period |
| `period`  | `int` | `60`    | Time period in seconds                        |

**Returns**: `Callable[[F], F]` - Decorated function that respects rate limits

**Behavior**:

- Tracks function calls within rolling time window
- Automatically sleeps and retries when limit exceeded
- Logs rate limit events with structured context
- Transparent to caller (no exceptions raised)

**Example**:

```python
from socratic_sofa.rate_limiter import rate_limited

# Default limits: 10 calls per 60 seconds
@rate_limited()
def call_api(endpoint: str) -> dict:
    """Make API call with rate limiting."""
    return requests.get(endpoint).json()

# Custom limits: 5 calls per 30 seconds
@rate_limited(calls=5, period=30)
def call_expensive_api(data: dict) -> dict:
    """Make expensive API call with stricter limits."""
    return requests.post(API_URL, json=data).json()

# Usage - automatically handles rate limiting
for i in range(20):
    result = call_api("/endpoint")  # Sleeps when limit reached
```

**Logging**:

```python
# On each call (DEBUG level)
logger.debug(
    "Rate-limited call",
    extra={
        "function": "call_api",
        "calls": 10,
        "period": 60
    }
)

# When limit reached (automatic, handled by library)
# Sleeps and retries with exponential backoff
```

**Multiple Limits**:

```python
# Different limits for different functions
@rate_limited(calls=100, period=3600)  # 100/hour
def batch_operation():
    ...

@rate_limited(calls=10, period=60)  # 10/minute
def interactive_operation():
    ...

@rate_limited(calls=1, period=1)  # 1/second
def real_time_operation():
    ...
```

---

### `rate_limited_no_retry()`

Decorator that applies rate limiting without automatic retry (fail fast).

**Signature**:

```python
def rate_limited_no_retry(calls: int = DEFAULT_CALLS, period: int = DEFAULT_PERIOD) -> Callable[[F], F]
```

**Parameters**:

| Parameter | Type  | Default | Description                                   |
| --------- | ----- | ------- | --------------------------------------------- |
| `calls`   | `int` | `10`    | Maximum number of calls allowed in the period |
| `period`  | `int` | `60`    | Time period in seconds                        |

**Returns**: `Callable[[F], F]` - Decorated function that raises on rate limit

**Behavior**:

- Tracks function calls within rolling time window
- Raises `RateLimitException` immediately when limit exceeded
- Caller must handle the exception
- Useful for time-sensitive operations

**Example**:

```python
from socratic_sofa.rate_limiter import rate_limited_no_retry, RateLimitException

@rate_limited_no_retry(calls=5, period=60)
def time_sensitive_api_call(data: dict) -> dict:
    """Make API call that must fail fast on rate limit."""
    return requests.post(API_URL, json=data).json()

# Usage with exception handling
try:
    result = time_sensitive_api_call({"query": "test"})
except RateLimitException:
    # Handle rate limit gracefully
    logger.warning("Rate limit exceeded, using cached data")
    result = get_cached_result()
```

**Use Cases**:

1. **Real-Time Operations**: When waiting is not acceptable
2. **User-Facing APIs**: Provide immediate feedback
3. **Fallback Logic**: Use alternative data sources
4. **Circuit Breakers**: Detect overload conditions

```python
@rate_limited_no_retry(calls=10, period=60)
def get_fresh_data():
    return fetch_from_api()

def get_data_with_fallback():
    """Get data with automatic fallback on rate limit."""
    try:
        return get_fresh_data()
    except RateLimitException:
        logger.info("Using cached data due to rate limit")
        return get_cached_data()
```

---

## Exception

### `RateLimitException`

Exception raised when rate limit is exceeded (re-exported from `ratelimit` library).

**Import**:

```python
from socratic_sofa.rate_limiter import RateLimitException
```

**Usage**:

```python
try:
    result = rate_limited_function()
except RateLimitException as e:
    logger.warning("Rate limit hit", extra={"error": str(e)})
    # Handle gracefully
```

**Note**: Only raised by `@rate_limited_no_retry()`. The `@rate_limited()` decorator handles this internally with automatic retry.

---

## Constants

### `DEFAULT_CALLS`

Default maximum number of calls allowed: `10`

### `DEFAULT_PERIOD`

Default time period in seconds: `60`

**Usage**:

```python
from socratic_sofa.rate_limiter import DEFAULT_CALLS, DEFAULT_PERIOD

# Use defaults explicitly
@rate_limited(calls=DEFAULT_CALLS, period=DEFAULT_PERIOD)
def my_function():
    ...

# Or just omit for same effect
@rate_limited()
def my_function():
    ...
```

---

## Complete Integration Example

### Content Moderation with Rate Limiting

```python
from socratic_sofa.logging_config import get_logger, log_timing
from socratic_sofa.rate_limiter import rate_limited, RateLimitException
from anthropic import Anthropic

logger = get_logger(__name__)

@rate_limited(calls=10, period=60)
def is_topic_appropriate(topic: str) -> tuple[bool, str]:
    """
    Check topic appropriateness with rate limiting.

    Rate limited to 10 calls per 60 seconds with automatic retry.
    """
    logger.info("Checking topic", extra={"topic": topic[:50]})

    with log_timing(logger, "moderation_api_call"):
        client = Anthropic()
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=100,
            messages=[{"role": "user", "content": f"Moderate: {topic}"}]
        )

    result = response.content[0].text.strip()
    is_ok = result.startswith("APPROPRIATE")

    logger.info(
        "Moderation complete",
        extra={"result": "approved" if is_ok else "rejected"}
    )

    return is_ok, "" if is_ok else "Topic may not be appropriate"

# Usage - automatic rate limiting with retry
for topic in topics:
    is_ok, reason = is_topic_appropriate(topic)
    # Function automatically waits if rate limit reached
```

### Time-Sensitive Operation with Fallback

```python
from socratic_sofa.rate_limiter import rate_limited_no_retry, RateLimitException

@rate_limited_no_retry(calls=5, period=60)
def fetch_live_suggestions() -> list[str]:
    """Fetch suggestions from API (fail fast on rate limit)."""
    response = requests.get(SUGGESTIONS_API)
    return response.json()["suggestions"]

def get_topic_suggestions() -> list[str]:
    """Get suggestions with automatic fallback."""
    try:
        # Try live API first
        return fetch_live_suggestions()
    except RateLimitException:
        # Fall back to static suggestions
        logger.info("Rate limit exceeded, using static suggestions")
        return [
            "What is justice?",
            "What is the good life?",
            "Is morality relative or universal?"
        ]

# Usage
suggestions = get_topic_suggestions()  # Always succeeds
```

---

## Advanced Patterns

### Class Method Rate Limiting

```python
class ContentModerator:
    def __init__(self):
        self.logger = get_logger(__name__)

    @rate_limited(calls=10, period=60)
    def moderate(self, content: str) -> bool:
        """Moderate content with rate limiting."""
        # Rate limit applies per-instance
        return self._check_content(content)

    @rate_limited_no_retry(calls=5, period=30)
    def moderate_urgent(self, content: str) -> bool:
        """Urgent moderation (fail fast)."""
        return self._check_content(content)

# Usage
moderator = ContentModerator()
is_ok = moderator.moderate(content)  # Automatic retry
```

### Conditional Rate Limiting

```python
def rate_limit_if_prod(func):
    """Apply rate limiting only in production."""
    if os.getenv("ENVIRONMENT") == "production":
        return rate_limited(calls=10, period=60)(func)
    return func

@rate_limit_if_prod
def api_call():
    """Rate limited in production, unlimited in dev."""
    ...
```

### Multiple Rate Limits (Tiered)

```python
from functools import wraps

def multi_rate_limit(func):
    """Apply multiple rate limits (minute, hour, day)."""

    # Inner decorators
    @rate_limited(calls=10, period=60)      # 10/minute
    @rate_limited(calls=100, period=3600)   # 100/hour
    @rate_limited(calls=1000, period=86400) # 1000/day
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

@multi_rate_limit
def api_call():
    """Respects all three limits."""
    ...
```

### Rate Limit Monitoring

```python
from socratic_sofa.logging_config import get_logger
from socratic_sofa.rate_limiter import rate_limited, RateLimitException

logger = get_logger(__name__)

class RateLimitMonitor:
    """Monitor rate limit usage."""

    def __init__(self):
        self.hit_count = 0
        self.call_count = 0

    def track_call(self, func):
        """Decorator to track rate limit hits."""
        @rate_limited_no_retry(calls=10, period=60)
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.call_count += 1
            try:
                return func(*args, **kwargs)
            except RateLimitException:
                self.hit_count += 1
                logger.warning(
                    "Rate limit hit",
                    extra={
                        "function": func.__name__,
                        "hit_rate": self.hit_count / self.call_count
                    }
                )
                raise

        return wrapper

# Usage
monitor = RateLimitMonitor()

@monitor.track_call
def monitored_api_call():
    ...
```

---

## Best Practices

### 1. Choose Appropriate Limits

```python
# ✅ Good: Reasonable limits matching API quotas
@rate_limited(calls=10, period=60)  # 10/minute
def content_moderation():
    ...

# ❌ Bad: Too permissive (may hit API limits)
@rate_limited(calls=1000, period=1)
def content_moderation():
    ...
```

### 2. Use Retry for Background Tasks

```python
# ✅ Good: Automatic retry for batch processing
@rate_limited(calls=5, period=60)
def batch_process_topics(topics: list[str]):
    for topic in topics:
        moderate(topic)  # Sleeps and retries automatically

# ❌ Bad: No retry for user-facing API
@rate_limited_no_retry()
def interactive_moderation(topic: str):
    # User waits or sees error
    ...
```

### 3. Handle Exceptions Gracefully

```python
# ✅ Good: Graceful degradation
@rate_limited_no_retry()
def get_fresh_data():
    ...

try:
    data = get_fresh_data()
except RateLimitException:
    logger.warning("Using cached data")
    data = get_cached_data()

# ❌ Bad: Unhandled exception
@rate_limited_no_retry()
def critical_api():
    ...

data = critical_api()  # May crash
```

### 4. Log Rate Limit Events

```python
# ✅ Good: Structured logging
@rate_limited(calls=10, period=60)
def moderation_call(topic: str):
    logger.debug("API call", extra={"topic": topic[:50]})
    # Rate limiter automatically logs when limit hit
    ...

# ❌ Bad: No visibility into rate limiting
@rate_limited()
def silent_call():
    # No logging, hard to debug issues
    ...
```

---

## Notes

- Rate limits are per-function, not global
- Limits are tracked in memory (not persistent across restarts)
- Use `@rate_limited()` for background/batch operations
- Use `@rate_limited_no_retry()` for interactive/time-sensitive operations
- Combine with `log_timing()` for complete operation visibility
- Thread-safe for concurrent usage
- Integrates seamlessly with structured logging
