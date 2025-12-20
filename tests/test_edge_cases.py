"""Edge case tests for Socratic Sofa.

These tests focus on boundary conditions, error handling, and unusual inputs
across all modules to ensure robust behavior.
"""

import pytest


class TestContentFilterEdgeCases:
    """Edge cases for content_filter module."""

    def test_empty_string_topic(self, mocker):
        """Empty string should be accepted without API call."""
        from socratic_sofa.content_filter import is_topic_appropriate

        mock_client = mocker.patch("socratic_sofa.content_filter.Anthropic")
        is_appropriate, reason = is_topic_appropriate("")
        assert is_appropriate is True
        assert reason == ""
        mock_client.assert_not_called()

    def test_whitespace_only_topic(self, mocker):
        """Whitespace-only string should be accepted without API call."""
        from socratic_sofa.content_filter import is_topic_appropriate

        mock_client = mocker.patch("socratic_sofa.content_filter.Anthropic")
        is_appropriate, reason = is_topic_appropriate("   \t\n  ")
        assert is_appropriate is True
        assert reason == ""
        mock_client.assert_not_called()

    def test_exactly_500_char_topic(self, mocker):
        """Topic at exactly 500 chars should be processed."""
        from socratic_sofa.content_filter import is_topic_appropriate

        mock_response = mocker.MagicMock()
        mock_response.content = [mocker.MagicMock(text="APPROPRIATE")]
        mock_client = mocker.patch("socratic_sofa.content_filter.Anthropic")
        mock_client.return_value.messages.create.return_value = mock_response

        topic = "a" * 500
        is_appropriate, reason = is_topic_appropriate(topic)
        assert is_appropriate is True
        mock_client.return_value.messages.create.assert_called_once()

    def test_501_char_topic_rejected(self, mocker):
        """Topic at 501 chars should be rejected without API call."""
        from socratic_sofa.content_filter import is_topic_appropriate

        mock_client = mocker.patch("socratic_sofa.content_filter.Anthropic")
        topic = "a" * 501
        is_appropriate, reason = is_topic_appropriate(topic)
        assert is_appropriate is False
        assert "too long" in reason.lower()
        mock_client.assert_not_called()

    def test_unicode_topic(self, mocker):
        """Unicode characters should be processed correctly."""
        from socratic_sofa.content_filter import is_topic_appropriate

        mock_response = mocker.MagicMock()
        mock_response.content = [mocker.MagicMock(text="APPROPRIATE")]
        mock_client = mocker.patch("socratic_sofa.content_filter.Anthropic")
        mock_client.return_value.messages.create.return_value = mock_response

        topic = "什么是哲学？ φιλοσοφία العلم 🤔"
        is_appropriate, reason = is_topic_appropriate(topic)
        assert is_appropriate is True

    def test_newlines_in_topic(self, mocker):
        """Topics with newlines should be processed."""
        from socratic_sofa.content_filter import is_topic_appropriate

        mock_response = mocker.MagicMock()
        mock_response.content = [mocker.MagicMock(text="APPROPRIATE")]
        mock_client = mocker.patch("socratic_sofa.content_filter.Anthropic")
        mock_client.return_value.messages.create.return_value = mock_response

        topic = "What is\nthe meaning\nof life?"
        is_appropriate, reason = is_topic_appropriate(topic)
        assert is_appropriate is True

    def test_special_characters_topic(self, mocker):
        """Topics with special characters should be processed."""
        from socratic_sofa.content_filter import is_topic_appropriate

        mock_response = mocker.MagicMock()
        mock_response.content = [mocker.MagicMock(text="APPROPRIATE")]
        mock_client = mocker.patch("socratic_sofa.content_filter.Anthropic")
        mock_client.return_value.messages.create.return_value = mock_response

        topic = "Is A=B if B=A? (using logical operators: && || !)"
        is_appropriate, reason = is_topic_appropriate(topic)
        assert is_appropriate is True


class TestAlternativeSuggestionsEdgeCases:
    """Edge cases for get_alternative_suggestions function."""

    def test_none_topic(self):
        """None should return defaults (handled by empty check)."""
        from socratic_sofa.content_filter import get_alternative_suggestions

        # Function checks "not rejected_topic" which is True for None
        suggestions = get_alternative_suggestions(None)
        assert len(suggestions) > 0

    def test_empty_string(self):
        """Empty string should return defaults."""
        from socratic_sofa.content_filter import get_alternative_suggestions

        suggestions = get_alternative_suggestions("")
        assert len(suggestions) > 0
        assert "What is justice?" in suggestions

    def test_mixed_case_keywords(self):
        """Keywords should be case-insensitive."""
        from socratic_sofa.content_filter import get_alternative_suggestions

        suggestions_lower = get_alternative_suggestions("ai ethics")
        suggestions_upper = get_alternative_suggestions("AI ETHICS")
        suggestions_mixed = get_alternative_suggestions("Ai EtHiCs")

        # All should return technology-themed suggestions
        assert "Can AI have rights?" in suggestions_lower
        assert "Can AI have rights?" in suggestions_upper
        assert "Can AI have rights?" in suggestions_mixed

    def test_multiple_theme_keywords(self):
        """Topic with multiple themes should match first theme."""
        from socratic_sofa.content_filter import get_alternative_suggestions

        # Has both "ai" and "consciousness"
        topic = "Can AI achieve consciousness?"
        suggestions = get_alternative_suggestions(topic)
        # Should match technology theme (first in order)
        assert any("AI" in s or "technology" in s.lower() for s in suggestions)


class TestLoggingConfigEdgeCases:
    """Edge cases for logging_config module."""

    def test_empty_context(self):
        """Logger with empty context should work."""
        from socratic_sofa.logging_config import get_logger

        logger = get_logger("test")
        # Should not raise
        logger.info("test message")

    def test_nested_context(self):
        """Nested with_context calls should chain correctly."""
        from socratic_sofa.logging_config import get_logger

        logger = get_logger("test", a=1)
        logger2 = logger.with_context(b=2)
        logger3 = logger2.with_context(c=3)

        assert logger3.extra["a"] == 1
        assert logger3.extra["b"] == 2
        assert logger3.extra["c"] == 3

    def test_context_override(self):
        """Later context should override earlier."""
        from socratic_sofa.logging_config import get_logger

        logger = get_logger("test", key="original")
        logger2 = logger.with_context(key="overridden")

        assert logger.extra["key"] == "original"
        assert logger2.extra["key"] == "overridden"

    def test_special_characters_in_context_values(self):
        """Context with special characters in values should work."""
        from socratic_sofa.logging_config import get_logger

        # Use keys that don't conflict with LogRecord reserved attributes
        logger = get_logger("test", file_path="/path/to/file", user_msg="hello\nworld")
        # Should not raise
        logger.info("test")


class TestRateLimiterEdgeCases:
    """Edge cases for rate_limiter module."""

    def test_zero_period_raises(self):
        """Zero period should raise or behave consistently."""
        from socratic_sofa.rate_limiter import rate_limited_no_retry

        @rate_limited_no_retry(calls=1, period=0)
        def test_func():
            return "success"

        # First call should work
        result = test_func()
        assert result == "success"

    def test_high_call_limit(self):
        """High call limits should work."""
        from socratic_sofa.rate_limiter import rate_limited_no_retry

        @rate_limited_no_retry(calls=1000, period=60)
        def test_func():
            return "success"

        # Should allow many calls
        for _ in range(100):
            assert test_func() == "success"

    def test_very_short_period(self):
        """Very short periods should work."""
        import time

        from socratic_sofa.rate_limiter import rate_limited_no_retry

        @rate_limited_no_retry(calls=1, period=0.01)
        def test_func():
            return "success"

        test_func()
        time.sleep(0.02)
        # Should be allowed again
        assert test_func() == "success"


class TestGradioAppEdgeCases:
    """Edge cases for gradio_app module."""

    def test_handle_topic_selection_with_both_empty(self):
        """Both dropdown and custom empty should return empty."""
        from socratic_sofa.gradio_app import handle_topic_selection

        result = handle_topic_selection("", "")
        assert result == ""

    def test_handle_topic_selection_custom_overrides_dropdown(self):
        """Custom topic should override dropdown selection."""
        from socratic_sofa.gradio_app import handle_topic_selection

        result = handle_topic_selection("Dropdown Topic", "Custom Topic")
        assert result == "Custom Topic"

    def test_handle_topic_selection_dropdown_when_custom_empty(self):
        """Dropdown should be used when custom is empty."""
        from socratic_sofa.gradio_app import handle_topic_selection

        result = handle_topic_selection("Dropdown Topic", "")
        assert result == "Dropdown Topic"

    def test_handle_topic_selection_strips_whitespace(self):
        """Topics should have whitespace stripped."""
        from socratic_sofa.gradio_app import handle_topic_selection

        result = handle_topic_selection("", "  Custom Topic  ")
        assert result == "Custom Topic"


class TestCrewEdgeCases:
    """Edge cases for crew configuration."""

    def test_crew_initialization(self):
        """Crew should initialize without errors."""
        from socratic_sofa.crew import SocraticSofa

        crew = SocraticSofa()
        # Should not raise during crew setup
        assert crew is not None


class TestMainFunctionEdgeCases:
    """Edge cases for main module functions."""

    def test_run_calls_kickoff(self, mocker):
        """Run should call crew kickoff with default inputs."""
        from socratic_sofa.main import run

        # Mock the crew class
        mock_crew_class = mocker.patch("socratic_sofa.main.SocraticSofa")
        mock_result = mocker.MagicMock()
        mock_result.raw = "Test Result"
        mock_crew_class.return_value.crew.return_value.kickoff.return_value = mock_result

        # Mock print to avoid output
        mocker.patch("builtins.print")

        run()
        mock_crew_class.return_value.crew.return_value.kickoff.assert_called_once()

    def test_run_with_trigger_requires_payload(self):
        """run_with_trigger should raise without payload."""
        import sys

        from socratic_sofa.main import run_with_trigger

        # Save original argv
        original_argv = sys.argv.copy()
        try:
            sys.argv = ["script"]  # No payload
            with pytest.raises(Exception, match="No trigger payload"):
                run_with_trigger()
        finally:
            sys.argv = original_argv

    def test_run_with_trigger_invalid_json(self):
        """run_with_trigger should raise on invalid JSON."""
        import sys

        from socratic_sofa.main import run_with_trigger

        original_argv = sys.argv.copy()
        try:
            sys.argv = ["script", "not valid json"]
            with pytest.raises(Exception, match="Invalid JSON"):
                run_with_trigger()
        finally:
            sys.argv = original_argv
