"""
Rate limiting for API calls in Socratic Sofa.

Uses the ratelimit library to prevent excessive API calls
to the Anthropic content moderation endpoint.
"""

from functools import wraps
from collections.abc import Callable
from typing import Any, TypeVar

from ratelimit import RateLimitException, limits, sleep_and_retry

from socratic_sofa.logging_config import get_logger

logger = get_logger(__name__)

# Default rate limit: 10 calls per 60 seconds
DEFAULT_CALLS = 10
DEFAULT_PERIOD = 60

F = TypeVar("F", bound=Callable[..., Any])


def rate_limited(calls: int = DEFAULT_CALLS, period: int = DEFAULT_PERIOD) -> Callable[[F], F]:
    """
    Decorator that applies rate limiting with automatic retry.

    Args:
        calls: Maximum number of calls allowed in the period
        period: Time period in seconds

    Returns:
        Decorated function that respects rate limits
    """

    def decorator(func: F) -> F:
        @sleep_and_retry
        @limits(calls=calls, period=period)
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.debug(
                "Rate-limited call",
                extra={"function": func.__name__, "calls": calls, "period": period},
            )
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def rate_limited_no_retry(
    calls: int = DEFAULT_CALLS, period: int = DEFAULT_PERIOD
) -> Callable[[F], F]:
    """
    Decorator that applies rate limiting without automatic retry.

    Raises RateLimitException if the rate limit is exceeded.

    Args:
        calls: Maximum number of calls allowed in the period
        period: Time period in seconds

    Returns:
        Decorated function that respects rate limits
    """

    def decorator(func: F) -> F:
        @limits(calls=calls, period=period)
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.debug(
                "Rate-limited call (no retry)",
                extra={"function": func.__name__, "calls": calls, "period": period},
            )
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


# Re-export RateLimitException for convenience
__all__ = ["rate_limited", "rate_limited_no_retry", "RateLimitException", "DEFAULT_CALLS", "DEFAULT_PERIOD"]
