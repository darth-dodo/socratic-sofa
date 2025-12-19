"""
Unit tests for content_filter module.
Tests content moderation and alternative suggestions functionality.
"""

from unittest.mock import Mock

import pytest

from socratic_sofa.content_filter import get_alternative_suggestions, is_topic_appropriate


class TestIsTopicAppropriate:
    """Test suite for is_topic_appropriate function."""

    @pytest.fixture
    def mock_anthropic(self, mocker):
        """Fixture to mock Anthropic client."""
        mock_client = Mock()
        mock_response = Mock()
        mock_content = Mock()

        # Set up nested mock structure for response.content[0].text
        mock_content.text = "APPROPRIATE"
        mock_response.content = [mock_content]
        mock_client.messages.create.return_value = mock_response

        # Mock the Anthropic class constructor
        mocker.patch("socratic_sofa.content_filter.Anthropic", return_value=mock_client)

        return mock_client, mock_content

    def test_empty_topic_returns_appropriate(self):
        """Test that empty topic returns (True, '')."""
        is_appropriate, reason = is_topic_appropriate("")
        assert is_appropriate is True
        assert reason == ""

    def test_whitespace_topic_returns_appropriate(self):
        """Test that whitespace-only topic returns (True, '')."""
        is_appropriate, reason = is_topic_appropriate("   \t\n  ")
        assert is_appropriate is True
        assert reason == ""

    def test_topic_over_500_chars_returns_inappropriate(self):
        """Test that topic over 500 characters returns (False, error message)."""
        long_topic = "x" * 501
        is_appropriate, reason = is_topic_appropriate(long_topic)

        assert is_appropriate is False
        assert "too long" in reason.lower()
        assert "500 characters" in reason

    def test_topic_exactly_500_chars_is_acceptable(self, mock_anthropic):
        """Test that topic with exactly 500 characters passes length check."""
        mock_client, mock_content = mock_anthropic
        mock_content.text = "APPROPRIATE"

        topic_500 = "x" * 500
        is_appropriate, reason = is_topic_appropriate(topic_500)

        assert is_appropriate is True
        assert reason == ""
        # Verify API was called
        assert mock_client.messages.create.called

    def test_appropriate_response_returns_true(self, mock_anthropic):
        """Test that 'APPROPRIATE' response returns (True, '')."""
        mock_client, mock_content = mock_anthropic
        mock_content.text = "APPROPRIATE"

        is_appropriate, reason = is_topic_appropriate("What is justice?")

        assert is_appropriate is True
        assert reason == ""

    def test_inappropriate_response_returns_false_with_reason(self, mock_anthropic):
        """Test that 'INAPPROPRIATE: reason' response returns (False, reason)."""
        mock_client, mock_content = mock_anthropic
        mock_content.text = "INAPPROPRIATE: Contains explicit content"

        is_appropriate, reason = is_topic_appropriate("inappropriate topic")

        assert is_appropriate is False
        assert "This topic may not be appropriate:" in reason
        assert "Contains explicit content" in reason

    def test_inappropriate_response_with_extra_whitespace(self, mock_anthropic):
        """Test that inappropriate response handles whitespace correctly."""
        mock_client, mock_content = mock_anthropic
        mock_content.text = "INAPPROPRIATE:   Hate speech   "

        is_appropriate, reason = is_topic_appropriate("hate topic")

        assert is_appropriate is False
        assert "Hate speech" in reason

    def test_unclear_response_returns_true(self, mock_anthropic):
        """Test that unclear/unexpected response returns (True, '') - fail open."""
        mock_client, mock_content = mock_anthropic
        mock_content.text = "MAYBE"

        is_appropriate, reason = is_topic_appropriate("ambiguous topic")

        assert is_appropriate is True
        assert reason == ""

    def test_partial_match_appropriate_returns_true(self, mock_anthropic):
        """Test that response starting with 'APPROPRIATE' returns True."""
        mock_client, mock_content = mock_anthropic
        mock_content.text = "APPROPRIATE for discussion"

        is_appropriate, reason = is_topic_appropriate("some topic")

        assert is_appropriate is True
        assert reason == ""

    def test_api_exception_returns_true_fail_open(self, mocker, capsys):
        """Test that API exception returns (True, '') to fail open."""
        # Mock Anthropic to raise an exception
        mocker.patch(
            "socratic_sofa.content_filter.Anthropic", side_effect=Exception("API Error")
        )

        is_appropriate, reason = is_topic_appropriate("some topic")

        assert is_appropriate is True
        assert reason == ""

        # Check that error was printed
        captured = capsys.readouterr()
        assert "Content moderation error" in captured.out

    def test_api_network_error_returns_true(self, mocker, capsys):
        """Test that network errors fail open gracefully."""
        mocker.patch(
            "socratic_sofa.content_filter.Anthropic",
            side_effect=ConnectionError("Network unavailable"),
        )

        is_appropriate, reason = is_topic_appropriate("test topic")

        assert is_appropriate is True
        assert reason == ""

        captured = capsys.readouterr()
        assert "Content moderation error" in captured.out

    def test_api_called_with_correct_parameters(self, mock_anthropic):
        """Test that Anthropic API is called with correct parameters."""
        mock_client, mock_content = mock_anthropic
        mock_content.text = "APPROPRIATE"

        topic = "Is morality objective?"
        is_topic_appropriate(topic)

        # Verify API call parameters
        call_args = mock_client.messages.create.call_args
        assert call_args is not None

        kwargs = call_args[1]
        assert kwargs["model"] == "claude-3-5-haiku-20241022"
        assert kwargs["max_tokens"] == 100
        assert len(kwargs["messages"]) == 1
        assert kwargs["messages"][0]["role"] == "user"
        assert topic in kwargs["messages"][0]["content"]

    def test_moderation_prompt_includes_topic(self, mock_anthropic):
        """Test that the moderation prompt includes the topic being evaluated."""
        mock_client, mock_content = mock_anthropic
        mock_content.text = "APPROPRIATE"

        topic = "Do we have free will?"
        is_topic_appropriate(topic)

        call_args = mock_client.messages.create.call_args
        prompt = call_args[1]["messages"][0]["content"]

        assert topic in prompt
        assert "content moderator" in prompt.lower()
        assert "philosophical" in prompt.lower()

    def test_multiple_calls_with_different_topics(self, mock_anthropic):
        """Test multiple calls work correctly with different topics."""
        mock_client, mock_content = mock_anthropic

        # First call - appropriate
        mock_content.text = "APPROPRIATE"
        is_appropriate1, reason1 = is_topic_appropriate("What is truth?")
        assert is_appropriate1 is True

        # Second call - inappropriate
        mock_content.text = "INAPPROPRIATE: Explicit content"
        is_appropriate2, reason2 = is_topic_appropriate("bad topic")
        assert is_appropriate2 is False
        assert "Explicit content" in reason2

        # Verify both calls were made
        assert mock_client.messages.create.call_count == 2


class TestGetAlternativeSuggestions:
    """Test suite for get_alternative_suggestions function."""

    def test_returns_non_empty_list(self):
        """Test that function returns a non-empty list."""
        suggestions = get_alternative_suggestions()

        assert isinstance(suggestions, list)
        assert len(suggestions) > 0

    def test_all_items_are_strings(self):
        """Test that all items in the list are strings."""
        suggestions = get_alternative_suggestions()

        assert all(isinstance(item, str) for item in suggestions)

    def test_all_strings_are_non_empty(self):
        """Test that all suggested topics are non-empty strings."""
        suggestions = get_alternative_suggestions()

        assert all(len(item.strip()) > 0 for item in suggestions)

    def test_contains_expected_philosophical_topics(self):
        """Test that suggestions contain expected philosophical topics."""
        suggestions = get_alternative_suggestions()

        # Check for some expected topics
        expected_topics = [
            "What is justice?",
            "What is the good life?",
            "Is morality relative or universal?",
            "What is consciousness?",
            "Do we have free will?",
        ]

        for expected in expected_topics:
            assert expected in suggestions

    def test_contains_modern_philosophical_topics(self):
        """Test that suggestions include modern philosophical questions."""
        suggestions = get_alternative_suggestions()

        # Modern topics
        modern_topics = ["Can AI have rights?"]

        for modern in modern_topics:
            assert modern in suggestions

    def test_returns_same_list_on_multiple_calls(self):
        """Test that function returns consistent results across multiple calls."""
        suggestions1 = get_alternative_suggestions()
        suggestions2 = get_alternative_suggestions()

        assert suggestions1 == suggestions2

    def test_minimum_number_of_suggestions(self):
        """Test that there are at least 5 alternative suggestions."""
        suggestions = get_alternative_suggestions()

        assert len(suggestions) >= 5

    def test_suggestions_are_questions(self):
        """Test that most suggestions are formatted as questions."""
        suggestions = get_alternative_suggestions()

        # At least 80% should end with '?'
        question_count = sum(1 for s in suggestions if s.strip().endswith("?"))
        assert question_count >= len(suggestions) * 0.8
