"""Tests for rate_limiter module using ratelimit library."""

import time

import pytest
from ratelimit import RateLimitException

from socratic_sofa.rate_limiter import (
    DEFAULT_CALLS,
    DEFAULT_PERIOD,
    rate_limited,
    rate_limited_no_retry,
)


class TestRateLimited:
    """Tests for the rate_limited decorator."""

    def test_allows_calls_under_limit(self):
        """Calls under the limit should succeed."""
        call_count = 0

        @rate_limited(calls=5, period=60)
        def test_func():
            nonlocal call_count
            call_count += 1
            return "success"

        for _ in range(5):
            result = test_func()
            assert result == "success"

        assert call_count == 5

    def test_sleeps_and_retries_when_over_limit(self):
        """Should sleep and retry when rate limit exceeded."""
        call_count = 0

        @rate_limited(calls=2, period=1)
        def test_func():
            nonlocal call_count
            call_count += 1
            return call_count

        # First two calls should be immediate
        start = time.monotonic()
        test_func()
        test_func()
        # Third call should wait ~1 second
        test_func()
        elapsed = time.monotonic() - start

        assert call_count == 3
        # Should have waited approximately 1 second
        assert elapsed >= 0.9

    def test_preserves_function_metadata(self):
        """Decorator should preserve function name and docstring."""

        @rate_limited()
        def my_function():
            """My docstring."""
            pass

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring."

    def test_passes_arguments(self):
        """Decorator should pass arguments correctly."""

        @rate_limited(calls=10, period=60)
        def add(a, b):
            return a + b

        assert add(2, 3) == 5
        assert add(a=10, b=20) == 30

    def test_returns_value(self):
        """Decorator should return the function's return value."""

        @rate_limited(calls=10, period=60)
        def get_value():
            return {"key": "value"}

        result = get_value()
        assert result == {"key": "value"}


class TestRateLimitedNoRetry:
    """Tests for the rate_limited_no_retry decorator."""

    def test_allows_calls_under_limit(self):
        """Calls under the limit should succeed."""
        call_count = 0

        @rate_limited_no_retry(calls=3, period=60)
        def test_func():
            nonlocal call_count
            call_count += 1
            return "success"

        for _ in range(3):
            result = test_func()
            assert result == "success"

        assert call_count == 3

    def test_raises_exception_when_over_limit(self):
        """Should raise RateLimitException when limit exceeded."""

        @rate_limited_no_retry(calls=2, period=60)
        def test_func():
            return "success"

        # First two calls succeed
        test_func()
        test_func()

        # Third call should raise
        with pytest.raises(RateLimitException):
            test_func()

    def test_preserves_function_metadata(self):
        """Decorator should preserve function name and docstring."""

        @rate_limited_no_retry()
        def another_function():
            """Another docstring."""
            pass

        assert another_function.__name__ == "another_function"
        assert another_function.__doc__ == "Another docstring."

    def test_allows_after_period_expires(self):
        """Should allow calls after the period expires."""

        @rate_limited_no_retry(calls=2, period=1)
        def test_func():
            return "success"

        # Use up the limit
        test_func()
        test_func()

        # Should raise
        with pytest.raises(RateLimitException):
            test_func()

        # Wait for period to expire
        time.sleep(1.1)

        # Should work again
        result = test_func()
        assert result == "success"


class TestDefaultValues:
    """Tests for default configuration values."""

    def test_default_calls(self):
        """DEFAULT_CALLS should be 10."""
        assert DEFAULT_CALLS == 10

    def test_default_period(self):
        """DEFAULT_PERIOD should be 60."""
        assert DEFAULT_PERIOD == 60


class TestExceptionReexport:
    """Tests for re-exported RateLimitException."""

    def test_exception_is_importable(self):
        """RateLimitException should be importable from rate_limiter."""
        from socratic_sofa.rate_limiter import RateLimitException

        assert RateLimitException is not None

    def test_exception_is_catchable(self):
        """RateLimitException should be catchable."""
        from socratic_sofa.rate_limiter import RateLimitException

        @rate_limited_no_retry(calls=1, period=60)
        def test_func():
            return "success"

        test_func()

        try:
            test_func()
            pytest.fail("Should have raised RateLimitException")
        except RateLimitException:
            pass  # Expected
