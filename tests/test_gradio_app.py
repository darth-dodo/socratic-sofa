"""Unit tests for gradio_app.py helper functions.

Tests cover:
- Topic loading from YAML with error handling
- handle_topic_selection(): Topic selection priority logic
- Category filtering and random topic selection
"""

from pathlib import Path
from unittest.mock import mock_open

import pytest
import yaml

from socratic_sofa.gradio_app import (
    TOPICS,
    get_categories,
    get_random_topic,
    get_topics_by_category,
    get_topics_flat,
    handle_topic_selection,
    load_topics_data,
)


class TestLoadTopics:
    """Test suite for topic loading functions."""

    def test_returns_non_empty_list(self):
        """Should return a non-empty list of topics."""
        topics = TOPICS
        assert isinstance(topics, list)
        assert len(topics) > 0

    def test_topics_formatted_correctly(self):
        """Should format topics as '[Category] Topic'."""
        topics = TOPICS

        # Check that all topics follow the format
        for topic in topics:
            assert isinstance(topic, str)
            assert "]" in topic
            assert topic.startswith("[")

        # Verify specific examples based on topics.yaml
        assert "[Classic Philosophy] What is justice?" in topics
        assert "[Ethics & Morality] Is lying ever justified?" in topics
        assert "[Mind & Consciousness] What is consciousness?" in topics
        assert "[Society & Politics] What is freedom?" in topics
        assert "[Modern Dilemmas] Should AI have rights?" in topics

    def test_includes_multiple_categories(self):
        """Should include topics from multiple categories."""
        topics = TOPICS

        # Extract unique category names
        categories = set()
        for topic in topics:
            if "]" in topic:
                category = topic.split("]")[0].strip("[")
                categories.add(category)

        # Should have multiple categories
        assert len(categories) > 5
        assert "Classic Philosophy" in categories
        assert "Ethics & Morality" in categories
        assert "Fun & Quirky" in categories

    def test_fallback_on_file_error(self, mocker):
        """Should return default topics when file cannot be loaded."""
        # Mock Path to raise FileNotFoundError
        mock_path = mocker.patch("socratic_sofa.gradio_app.Path")
        mock_path.return_value.__truediv__.return_value = Path("/nonexistent/topics.yaml")

        # Mock open to raise exception
        mocker.patch("builtins.open", side_effect=FileNotFoundError("File not found"))

        topics_data = load_topics_data()

        # Should return default fallback topics data
        assert "fallback" in topics_data
        assert topics_data["fallback"]["name"] == "Philosophy"

    def test_fallback_on_yaml_parse_error(self, mocker):
        """Should return default topics when YAML parsing fails."""
        # Mock open to return invalid YAML
        invalid_yaml = "invalid: yaml: content: {"
        mocker.patch("builtins.open", mock_open(read_data=invalid_yaml))

        # Mock yaml.safe_load to raise exception
        mocker.patch("yaml.safe_load", side_effect=yaml.YAMLError("Parse error"))

        topics_data = load_topics_data()

        # Should return default fallback topics
        assert "fallback" in topics_data

    def test_fallback_on_generic_exception(self, mocker):
        """Should return default topics on any unexpected exception."""
        # Mock to raise a generic exception
        mocker.patch("builtins.open", side_effect=Exception("Unexpected error"))

        topics_data = load_topics_data()

        # Should return default fallback topics
        assert "fallback" in topics_data


class TestCategoryFunctions:
    """Test suite for category filtering functions."""

    def test_get_categories_returns_list(self):
        """Should return list of categories with 'All Categories' first."""
        topics_data = load_topics_data()
        categories = get_categories(topics_data)

        assert isinstance(categories, list)
        assert categories[0] == "All Categories"
        assert "Classic Philosophy" in categories

    def test_get_topics_flat_returns_formatted_list(self):
        """Should return flat list with category prefixes."""
        topics_data = load_topics_data()
        topics = get_topics_flat(topics_data)

        assert len(topics) > 0
        for topic in topics:
            assert "[" in topic and "]" in topic

    def test_get_topics_by_category_all(self):
        """Should return all topics for 'All Categories'."""
        topics_data = load_topics_data()
        topics = get_topics_by_category(topics_data, "All Categories")

        assert "✨ Let AI choose" in topics
        assert len(topics) > 50  # Many topics

    def test_get_topics_by_category_specific(self):
        """Should filter topics by specific category."""
        topics_data = load_topics_data()
        topics = get_topics_by_category(topics_data, "Classic Philosophy")

        assert "✨ Let AI choose" in topics
        for topic in topics[1:]:  # Skip AI choose
            assert "[Classic Philosophy]" in topic

    def test_get_random_topic_returns_valid_topic(self):
        """Should return a random topic from the library."""
        topics_data = load_topics_data()
        random_topic = get_random_topic(topics_data)

        assert isinstance(random_topic, str)
        assert "[" in random_topic and "]" in random_topic


class TestHandleTopicSelection:
    """Test suite for handle_topic_selection() function."""

    def test_textbox_takes_priority_over_dropdown(self):
        """Should prioritize textbox value when both are provided."""
        result = handle_topic_selection(
            dropdown_value="[Classic Philosophy] What is justice?",
            textbox_value="Should we colonize Mars?",
        )
        assert result == "Should we colonize Mars?"

    def test_textbox_priority_with_whitespace(self):
        """Should use textbox value even with extra whitespace."""
        result = handle_topic_selection(
            dropdown_value="[Classic Philosophy] What is justice?",
            textbox_value="  Should we colonize Mars?  ",
        )
        assert result == "Should we colonize Mars?"

    def test_empty_textbox_uses_dropdown(self):
        """Should use dropdown value when textbox is empty."""
        result = handle_topic_selection(
            dropdown_value="[Classic Philosophy] What is justice?", textbox_value=""
        )
        assert result == "What is justice?"

    def test_whitespace_only_textbox_uses_dropdown(self):
        """Should use dropdown value when textbox contains only whitespace."""
        result = handle_topic_selection(
            dropdown_value="[Classic Philosophy] What is justice?", textbox_value="   "
        )
        assert result == "What is justice?"

    def test_none_textbox_uses_dropdown(self):
        """Should use dropdown value when textbox is None."""
        result = handle_topic_selection(
            dropdown_value="[Classic Philosophy] What is justice?", textbox_value=None
        )
        assert result == "What is justice?"

    def test_ai_choose_returns_empty_string(self):
        """Should return empty string when '✨ Let AI choose' is selected."""
        result = handle_topic_selection(dropdown_value="✨ Let AI choose", textbox_value="")
        assert result == ""

    def test_ai_choose_overridden_by_textbox(self):
        """Should use textbox value even when dropdown is '✨ Let AI choose'."""
        result = handle_topic_selection(
            dropdown_value="✨ Let AI choose", textbox_value="What is consciousness?"
        )
        assert result == "What is consciousness?"

    def test_extracts_topic_from_category_format(self):
        """Should extract topic from '[Category] Topic' format."""
        result = handle_topic_selection(
            dropdown_value="[Classic Philosophy] What is justice?", textbox_value=""
        )
        assert result == "What is justice?"

        result = handle_topic_selection(
            dropdown_value="[Ethics & Morality] Is lying ever justified?", textbox_value=""
        )
        assert result == "Is lying ever justified?"

    def test_handles_multiple_brackets_in_topic(self):
        """Should handle topics that contain additional brackets."""
        result = handle_topic_selection(
            dropdown_value="[Fun & Quirky] If a tree falls [in a forest], does it make a sound?",
            textbox_value="",
        )
        # Should split on first "] " only
        assert result == "If a tree falls [in a forest], does it make a sound?"

    def test_returns_dropdown_value_if_no_category_format(self):
        """Should return dropdown value as-is if not in category format."""
        result = handle_topic_selection(dropdown_value="Plain topic text", textbox_value="")
        assert result == "Plain topic text"

    def test_empty_dropdown_returns_empty_string(self):
        """Should return empty string when dropdown is empty."""
        result = handle_topic_selection(dropdown_value="", textbox_value="")
        assert result == ""

    def test_none_dropdown_returns_empty_string(self):
        """Should return empty string when dropdown is None."""
        result = handle_topic_selection(dropdown_value=None, textbox_value="")
        assert result == ""

    def test_both_none_returns_empty_string(self):
        """Should return empty string when both inputs are None."""
        result = handle_topic_selection(dropdown_value=None, textbox_value=None)
        assert result == ""

    def test_both_empty_returns_empty_string(self):
        """Should return empty string when both inputs are empty."""
        result = handle_topic_selection(dropdown_value="", textbox_value="")
        assert result == ""

    def test_textbox_strips_whitespace(self):
        """Should strip leading and trailing whitespace from textbox."""
        result = handle_topic_selection(
            dropdown_value="[Classic Philosophy] What is justice?",
            textbox_value="\n\t  What is happiness?  \n\t",
        )
        assert result == "What is happiness?"

    @pytest.mark.parametrize(
        "textbox_input",
        [
            "What is justice?",
            "Should AI have rights?",
            "Is a hot dog a sandwich?",
            "What is the meaning of life?",
        ],
    )
    def test_various_textbox_inputs(self, textbox_input):
        """Should correctly handle various textbox inputs."""
        result = handle_topic_selection(
            dropdown_value="[Some Category] Some Topic", textbox_value=textbox_input
        )
        assert result == textbox_input

    @pytest.mark.parametrize(
        "dropdown_input,expected",
        [
            ("[Classic Philosophy] What is justice?", "What is justice?"),
            ("[Ethics & Morality] Is lying justified?", "Is lying justified?"),
            ("[Mind & Consciousness] What is the self?", "What is the self?"),
            ("[Society & Politics] What is freedom?", "What is freedom?"),
            ("[Modern Dilemmas] Should AI have rights?", "Should AI have rights?"),
        ],
    )
    def test_various_dropdown_formats(self, dropdown_input, expected):
        """Should correctly extract topics from various category formats."""
        result = handle_topic_selection(dropdown_value=dropdown_input, textbox_value="")
        assert result == expected
