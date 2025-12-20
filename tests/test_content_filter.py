"""
Unit tests for content_filter module.
Tests content moderation and alternative suggestions functionality.
"""

from unittest.mock import Mock

import pytest

from socratic_sofa.content_filter import (
    get_alternative_suggestions,
    get_rejection_guidelines,
    is_topic_appropriate,
)


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

    def test_api_exception_returns_true_fail_open(self, mocker, caplog):
        """Test that API exception returns (True, '') to fail open."""
        import logging

        # Mock Anthropic to raise an exception
        mocker.patch("socratic_sofa.content_filter.Anthropic", side_effect=Exception("API Error"))

        # Capture logs from the socratic_sofa logger hierarchy
        with caplog.at_level(logging.WARNING, logger="socratic_sofa"):
            is_appropriate, reason = is_topic_appropriate("some topic")

        assert is_appropriate is True
        assert reason == ""

        # Check that warning was logged (check message or formatted text)
        log_text = caplog.text
        assert "Content moderation error" in log_text or any(
            "Content moderation error" in record.message for record in caplog.records
        )

    def test_api_network_error_returns_true(self, mocker, caplog):
        """Test that network errors fail open gracefully."""
        import logging

        mocker.patch(
            "socratic_sofa.content_filter.Anthropic",
            side_effect=ConnectionError("Network unavailable"),
        )

        # Capture logs from the socratic_sofa logger hierarchy
        with caplog.at_level(logging.WARNING, logger="socratic_sofa"):
            is_appropriate, reason = is_topic_appropriate("test topic")

        assert is_appropriate is True
        assert reason == ""

        # Check that warning was logged (check message or formatted text)
        log_text = caplog.text
        assert "Content moderation error" in log_text or any(
            "Content moderation error" in record.message for record in caplog.records
        )

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

    def test_with_empty_rejected_topic(self):
        """Test that empty rejected topic returns default suggestions."""
        suggestions = get_alternative_suggestions("")

        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        assert "What is justice?" in suggestions

    def test_with_whitespace_rejected_topic(self):
        """Test that whitespace rejected topic returns default suggestions."""
        suggestions = get_alternative_suggestions("   \t\n  ")

        assert isinstance(suggestions, list)
        assert "What is justice?" in suggestions

    def test_technology_theme_suggestions(self):
        """Test that technology-themed topics get related suggestions."""
        tech_topics = [
            "Can AI destroy humanity?",
            "Should we ban robots?",
            "What about computer ethics?",
            "Is the internet making us dumber?",
            "Should we fear technology?",
        ]

        for topic in tech_topics:
            suggestions = get_alternative_suggestions(topic)

            # Should contain technology-related suggestions
            assert any(
                "AI" in s or "technology" in s or "machine" in s or "digital" in s
                for s in suggestions
            )
            # Verify it's returning the technology theme set
            assert "Can AI have rights?" in suggestions

    def test_ethics_theme_suggestions(self):
        """Test that ethics-themed topics get related suggestions."""
        ethics_topics = [
            "Is stealing always wrong?",
            "What makes an action moral?",
            "Should we help the poor?",
            "Are there ethical absolutes?",
            "What is virtue?",
        ]

        for topic in ethics_topics:
            suggestions = get_alternative_suggestions(topic)

            # Should contain ethics-related suggestions
            assert any(
                "moral" in s.lower() or "ethics" in s.lower() or "good" in s.lower()
                for s in suggestions
            )
            assert "Is morality relative or universal?" in suggestions

    def test_politics_theme_suggestions(self):
        """Test that politics-themed topics get related suggestions."""
        politics_topics = [
            "Should government control everything?",
            "What is the best form of democracy?",
            "Are there limits to freedom?",
            "What are our rights?",
            "How should society be organized?",
        ]

        for topic in politics_topics:
            suggestions = get_alternative_suggestions(topic)

            # Should contain politics-related suggestions
            assert any(
                "government" in s.lower()
                or "democracy" in s.lower()
                or "freedom" in s.lower()
                or "rights" in s.lower()
                for s in suggestions
            )
            assert "What is justice?" in suggestions

    def test_consciousness_theme_suggestions(self):
        """Test that consciousness-themed topics get related suggestions."""
        consciousness_topics = [
            "What is the mind?",
            "How does the brain work?",
            "Are we aware of everything we think?",
            "What is perception?",
            "Is consciousness an illusion?",
        ]

        for topic in consciousness_topics:
            suggestions = get_alternative_suggestions(topic)

            # Should contain consciousness-related suggestions
            assert "What is consciousness?" in suggestions
            assert any("mind" in s.lower() or "consciousness" in s.lower() for s in suggestions)

    def test_existential_theme_suggestions(self):
        """Test that existential-themed topics get related suggestions."""
        existential_topics = [
            "What is the meaning of life?",
            "Why do we exist?",
            "How should we face death?",
            "What is our purpose?",
            "Why is there suffering?",
        ]

        for topic in existential_topics:
            suggestions = get_alternative_suggestions(topic)

            # Should contain existential suggestions
            assert any(
                "meaning" in s.lower() or "life" in s.lower() or "purpose" in s.lower()
                for s in suggestions
            )
            assert "What is the good life?" in suggestions

    def test_knowledge_theme_suggestions(self):
        """Test that knowledge-themed topics get related suggestions."""
        knowledge_topics = [
            "What is truth?",
            "How do we prove things?",
            "Can we believe in science?",
            "What is evidence?",
            "How do we know anything?",
        ]

        for topic in knowledge_topics:
            suggestions = get_alternative_suggestions(topic)

            # Should contain knowledge-related suggestions
            assert "What is truth?" in suggestions
            assert any("knowledge" in s.lower() or "truth" in s.lower() for s in suggestions)

    def test_aesthetics_theme_suggestions(self):
        """Test that aesthetics-themed topics get related suggestions."""
        aesthetic_topics = [
            "What makes art beautiful?",
            "Is music universal?",
            "Can machines create art?",
            "What is beauty?",
            "Is culture relative?",
        ]

        for topic in aesthetic_topics:
            suggestions = get_alternative_suggestions(topic)

            # Should contain aesthetic suggestions
            assert any(
                "beauty" in s.lower()
                or "art" in s.lower()
                or "aesthetic" in s.lower()
                or "creative" in s.lower()
                for s in suggestions
            )
            assert "Is beauty objective?" in suggestions

    def test_unthemed_topic_returns_defaults(self):
        """Test that topics with no clear theme return default suggestions."""
        unthemed_topics = [
            "Random gibberish xyz",
            "Nonsense topic abc",
            "Unrelated content",
        ]

        for topic in unthemed_topics:
            suggestions = get_alternative_suggestions(topic)

            # Should return default suggestions
            assert "What is justice?" in suggestions
            assert "What is the good life?" in suggestions
            assert len(suggestions) >= 5

    def test_case_insensitive_theme_detection(self):
        """Test that theme detection is case-insensitive."""
        suggestions_lower = get_alternative_suggestions("what about ai technology")
        suggestions_upper = get_alternative_suggestions("WHAT ABOUT AI TECHNOLOGY")
        suggestions_mixed = get_alternative_suggestions("WhAt AbOuT Ai TechNOLogy")

        # All should return the same technology-themed suggestions
        assert suggestions_lower == suggestions_upper == suggestions_mixed
        assert "Can AI have rights?" in suggestions_lower

    def test_multiple_themes_returns_first_match(self):
        """Test that topics with multiple themes return the first matching theme."""
        topic = "Should AI have moral rights in a democratic society?"
        # Contains: AI (tech), moral (ethics), rights (politics)
        # Should match technology first since it's checked first
        suggestions = get_alternative_suggestions(topic)

        assert "Can AI have rights?" in suggestions

    def test_themed_suggestions_have_minimum_count(self):
        """Test that themed suggestions return at least 5 alternatives."""
        themes = [
            "AI technology",
            "moral ethics",
            "government politics",
            "consciousness mind",
            "meaning of life",
            "truth knowledge",
            "beauty art",
        ]

        for theme in themes:
            suggestions = get_alternative_suggestions(theme)
            assert len(suggestions) >= 5


class TestGetRejectionGuidelines:
    """Test suite for get_rejection_guidelines function."""

    def test_returns_non_empty_string(self):
        """Test that function returns a non-empty string."""
        guidelines = get_rejection_guidelines()

        assert isinstance(guidelines, str)
        assert len(guidelines.strip()) > 0

    def test_contains_markdown_formatting(self):
        """Test that guidelines contain markdown formatting."""
        guidelines = get_rejection_guidelines()

        # Should have markdown headers or bold text
        assert "**" in guidelines or "#" in guidelines

    def test_contains_welcome_criteria(self):
        """Test that guidelines explain what is welcome."""
        guidelines = get_rejection_guidelines()

        assert "welcome" in guidelines.lower() or "appropriate" in guidelines.lower()

    def test_contains_rejection_criteria(self):
        """Test that guidelines explain what is filtered."""
        guidelines = get_rejection_guidelines()

        assert "filter" in guidelines.lower() or "reject" in guidelines.lower()

    def test_contains_examples(self):
        """Test that guidelines provide concrete examples."""
        guidelines = get_rejection_guidelines()

        # Should contain some example or illustration
        # Looking for question marks or specific examples
        assert "?" in guidelines

    def test_mentions_philosophical_discourse(self):
        """Test that guidelines reference philosophical discourse."""
        guidelines = get_rejection_guidelines()

        assert "philosophical" in guidelines.lower() or "philosophy" in guidelines.lower()

    def test_provides_guidance_not_loopholes(self):
        """Test that guidelines provide general guidance without giving evasion hints."""
        guidelines = get_rejection_guidelines()

        # Should not contain overly specific instructions on how to rephrase
        # Check that it's educational rather than prescriptive
        assert len(guidelines) > 100  # Substantial content
        assert "rephrasing" in guidelines.lower() or "rephrase" in guidelines.lower()

    def test_guidelines_are_user_friendly(self):
        """Test that guidelines use friendly, accessible language."""
        guidelines = get_rejection_guidelines()

        # Should avoid overly technical or harsh language
        assert (
            "hate" not in guidelines.lower() or "hate speech" in guidelines.lower()
        )  # Context matters
        # Should use welcoming language
        assert "welcome" in guidelines.lower() or "explore" in guidelines.lower()
