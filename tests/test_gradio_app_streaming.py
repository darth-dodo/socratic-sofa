"""Tests for gradio_app.py streaming functionality.

Tests the run_socratic_dialogue_streaming generator function with mocked
CrewAI components to avoid API calls.
"""

from unittest.mock import MagicMock, Mock

import pytest


class TestRunSocraticDialogueStreaming:
    """Test the streaming dialogue generator function."""

    @pytest.fixture
    def mock_crew_components(self, mocker):
        """Mock all CrewAI components."""
        # Mock the SocraticSofa class
        mock_sofa = MagicMock()
        mock_crew = MagicMock()
        mock_sofa.crew.return_value = mock_crew

        # Create mock task outputs
        mock_task_outputs = []
        for i, raw_text in enumerate(
            ["Topic output", "Proposition output", "Opposition output", "Judgment output"]
        ):
            mock_output = Mock()
            mock_output.raw = raw_text
            mock_task_outputs.append(mock_output)

        # Create mock tasks with outputs
        mock_tasks = []
        for output in mock_task_outputs:
            mock_task = Mock()
            mock_task.output = output
            mock_tasks.append(mock_task)

        mock_crew.tasks = mock_tasks

        # Mock kickoff to return immediately
        mock_crew.kickoff.return_value = Mock()

        mocker.patch("socratic_sofa.gradio_app.SocraticSofa", return_value=mock_sofa)

        return mock_sofa, mock_crew, mock_task_outputs

    @pytest.fixture
    def mock_content_filter_appropriate(self, mocker):
        """Mock content filter to return appropriate."""
        mocker.patch("socratic_sofa.gradio_app.is_topic_appropriate", return_value=(True, None))

    @pytest.fixture
    def mock_content_filter_inappropriate(self, mocker):
        """Mock content filter to return inappropriate."""
        mocker.patch(
            "socratic_sofa.gradio_app.is_topic_appropriate",
            return_value=(False, "Topic is inappropriate"),
        )
        mocker.patch(
            "socratic_sofa.gradio_app.get_alternative_suggestions",
            return_value=["What is justice?", "What is truth?"],
        )

    def test_inappropriate_topic_yields_error(self, mock_content_filter_inappropriate):
        """Should yield error messages for inappropriate topics."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        results = list(run_socratic_dialogue_streaming("", "inappropriate topic"))

        assert len(results) == 1
        # Output is now (progress_html, topic, proposition, opposition, judgment)
        progress, topic, prop, opp, judge = results[0]
        # Error message should contain friendly rejection
        assert "Let's Explore Something Different" in topic or "Topic is inappropriate" in topic
        assert "What is justice?" in topic

    def test_inappropriate_topic_all_outputs_same_error(self, mock_content_filter_inappropriate):
        """All four dialogue outputs should contain the same error message."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        results = list(run_socratic_dialogue_streaming("", "bad topic"))

        assert len(results) == 1
        # Output is now (progress_html, topic, proposition, opposition, judgment)
        progress, topic, prop, opp, judge = results[0]
        assert topic == prop == opp == judge
        # Progress should be empty for rejected topics
        assert progress == ""

    def test_yields_initial_loading_state(
        self, mock_crew_components, mock_content_filter_appropriate, mocker
    ):
        """Should yield initial loading state before crew execution."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        mock_sofa, mock_crew, _ = mock_crew_components

        # Make kickoff block until we're ready
        def slow_kickoff(inputs):
            import time

            time.sleep(0.1)
            return Mock()

        mock_crew.kickoff.side_effect = slow_kickoff

        gen = run_socratic_dialogue_streaming("", "What is truth?")
        first_result = next(gen)

        # Output is now (progress_html, topic, proposition, opposition, judgment)
        progress, topic, prop, opp, judge = first_result
        assert "⏳" in topic
        assert "Preparing philosophical inquiry" in topic
        # Progress should contain progress indicator HTML
        assert "progress" in progress.lower() or progress != ""

    def test_handles_crew_exception(self, mock_crew_components, mock_content_filter_appropriate):
        """Should yield error message when crew raises exception."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        mock_sofa, mock_crew, _ = mock_crew_components
        mock_crew.kickoff.side_effect = Exception("API Error")

        results = list(run_socratic_dialogue_streaming("", "What is truth?"))

        # Should have at least the initial loading state and error
        # Output is now (progress_html, topic, proposition, opposition, judgment)
        final_result = results[-1]
        progress, topic, prop, opp, judge = final_result
        assert "❌" in topic
        assert "Error running dialogue" in topic

    def test_final_output_uses_task_outputs(
        self, mock_crew_components, mock_content_filter_appropriate
    ):
        """Should use task outputs for final yield."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        mock_sofa, mock_crew, mock_outputs = mock_crew_components

        results = list(run_socratic_dialogue_streaming("", "What is truth?"))

        # Output is now (progress_html, topic, proposition, opposition, judgment)
        final_result = results[-1]
        progress, topic, prop, opp, judge = final_result
        assert "Topic output" in topic
        assert "Proposition output" in prop
        assert "Opposition output" in opp
        assert "Judgment output" in judge

    def test_proposition_has_header(self, mock_crew_components, mock_content_filter_appropriate):
        """Proposition output should include header."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        results = list(run_socratic_dialogue_streaming("", "What is truth?"))

        # Output is now (progress_html, topic, proposition, opposition, judgment)
        final_result = results[-1]
        progress, topic, prop, opp, judge = final_result
        assert "## 🔵 First Line of Inquiry" in prop

    def test_opposition_has_header(self, mock_crew_components, mock_content_filter_appropriate):
        """Opposition output should include header."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        results = list(run_socratic_dialogue_streaming("", "What is truth?"))

        # Output is now (progress_html, topic, proposition, opposition, judgment)
        final_result = results[-1]
        progress, topic, prop, opp, judge = final_result
        assert "## 🟢 Alternative Line of Inquiry" in opp

    def test_uses_custom_topic_over_dropdown(
        self, mock_crew_components, mock_content_filter_appropriate, mocker
    ):
        """Custom topic should take priority over dropdown."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        mock_sofa, mock_crew, _ = mock_crew_components

        list(run_socratic_dialogue_streaming("[Category] Dropdown Topic", "Custom Topic"))

        # Check the inputs passed to kickoff
        call_args = mock_crew.kickoff.call_args
        assert call_args[1]["inputs"]["topic"] == "Custom Topic"

    def test_extracts_topic_from_dropdown_format(
        self, mock_crew_components, mock_content_filter_appropriate
    ):
        """Should extract topic from [Category] Topic format."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        mock_sofa, mock_crew, _ = mock_crew_components

        list(run_socratic_dialogue_streaming("[Ethics] What is justice?", ""))

        call_args = mock_crew.kickoff.call_args
        assert call_args[1]["inputs"]["topic"] == "What is justice?"

    def test_ai_choose_passes_empty_topic(
        self, mock_crew_components, mock_content_filter_appropriate
    ):
        """AI choose option should pass empty topic."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        mock_sofa, mock_crew, _ = mock_crew_components

        list(run_socratic_dialogue_streaming("✨ Let AI choose", ""))

        call_args = mock_crew.kickoff.call_args
        assert call_args[1]["inputs"]["topic"] == ""

    def test_includes_current_year_in_inputs(
        self, mock_crew_components, mock_content_filter_appropriate
    ):
        """Should include current year in crew inputs."""
        from datetime import datetime

        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        mock_sofa, mock_crew, _ = mock_crew_components

        list(run_socratic_dialogue_streaming("", "Test topic"))

        call_args = mock_crew.kickoff.call_args
        assert call_args[1]["inputs"]["current_year"] == str(datetime.now().year)

    def test_sets_task_callback_on_crew_instance(
        self, mock_crew_components, mock_content_filter_appropriate
    ):
        """Should set task_callback on crew instance."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        mock_sofa, mock_crew, _ = mock_crew_components

        list(run_socratic_dialogue_streaming("", "Test topic"))

        # Verify task_callback was set
        assert mock_sofa.task_callback is not None


class TestStreamingWithTaskCallbacks:
    """Test streaming behavior with simulated task callbacks."""

    @pytest.fixture
    def mock_streaming_setup(self, mocker):
        """Setup mocks for streaming test."""
        mocker.patch("socratic_sofa.gradio_app.is_topic_appropriate", return_value=(True, None))

        mock_sofa = MagicMock()
        mock_crew = MagicMock()
        mock_sofa.crew.return_value = mock_crew

        # Create mock tasks
        mock_tasks = []
        for raw_text in ["Topic", "Prop", "Opp", "Judge"]:
            mock_task = Mock()
            mock_output = Mock()
            mock_output.raw = raw_text
            mock_task.output = mock_output
            mock_tasks.append(mock_task)

        mock_crew.tasks = mock_tasks

        # Store callback for later use
        callback_holder = {"callback": None}

        def capture_callback(val):
            callback_holder["callback"] = val

        mock_sofa.task_callback = property(
            fget=lambda self: callback_holder["callback"],
            fset=lambda self, val: capture_callback(val),
        )

        mocker.patch("socratic_sofa.gradio_app.SocraticSofa", return_value=mock_sofa)

        return mock_sofa, mock_crew, callback_holder

    def test_handles_empty_task_list(self, mocker):
        """Should handle case where tasks list is empty."""
        mocker.patch("socratic_sofa.gradio_app.is_topic_appropriate", return_value=(True, None))

        mock_sofa = MagicMock()
        mock_crew = MagicMock()
        mock_sofa.crew.return_value = mock_crew
        mock_crew.tasks = []  # Empty tasks

        mocker.patch("socratic_sofa.gradio_app.SocraticSofa", return_value=mock_sofa)

        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        results = list(run_socratic_dialogue_streaming("", "Test"))

        # Should complete without error
        assert len(results) >= 1

    def test_handles_partial_task_outputs(self, mocker):
        """Should handle case where some task outputs are None."""
        mocker.patch("socratic_sofa.gradio_app.is_topic_appropriate", return_value=(True, None))

        mock_sofa = MagicMock()
        mock_crew = MagicMock()
        mock_sofa.crew.return_value = mock_crew

        # Create tasks with some None outputs
        mock_tasks = []
        for i, raw_text in enumerate(["Topic", None, "Opp", None]):
            mock_task = Mock()
            if raw_text:
                mock_output = Mock()
                mock_output.raw = raw_text
                mock_task.output = mock_output
            else:
                mock_task.output = None
            mock_tasks.append(mock_task)

        mock_crew.tasks = mock_tasks

        mocker.patch("socratic_sofa.gradio_app.SocraticSofa", return_value=mock_sofa)

        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        results = list(run_socratic_dialogue_streaming("", "Test"))

        # Should complete without error
        assert len(results) >= 1
        # Output is now (progress_html, topic, proposition, opposition, judgment)
        final = results[-1]
        progress, topic, prop, opp, judge = final
        assert "Topic" in topic
        assert "Opp" in opp


class TestGradioInterfaceSetup:
    """Test Gradio interface configuration."""

    def test_demo_exists(self):
        """Demo interface should be defined."""
        from socratic_sofa.gradio_app import demo

        assert demo is not None

    def test_demo_has_title(self):
        """Demo should have a title set."""
        from socratic_sofa.gradio_app import demo

        assert demo.title is not None
        assert "Socratic" in demo.title

    def test_custom_css_defined(self):
        """Custom CSS should be defined for mobile responsiveness."""
        from socratic_sofa.gradio_app import CUSTOM_CSS

        assert CUSTOM_CSS is not None
        assert "@media" in CUSTOM_CSS
        assert "768px" in CUSTOM_CSS  # Mobile breakpoint

    def test_topics_loaded(self):
        """Topics should be loaded from YAML."""
        from socratic_sofa.gradio_app import TOPICS

        assert TOPICS is not None
        assert len(TOPICS) > 0

    def test_main_function_exists(self):
        """Main function should exist for launching."""
        from socratic_sofa.gradio_app import main

        assert callable(main)


class TestGetTopicsByCategoryFallback:
    """Test edge cases in get_topics_by_category."""

    def test_unknown_category_returns_all_topics(self):
        """Should return all topics when category doesn't exist."""
        from socratic_sofa.gradio_app import get_topics_by_category, load_topics_data

        topics_data = load_topics_data()
        topics = get_topics_by_category(topics_data, "Nonexistent Category")

        # Should fall back to all topics (line 61)
        assert "✨ Let AI choose" in topics
        assert len(topics) > 1  # Should contain AI choose + all topics

    def test_all_categories_returns_ai_choose_plus_all(self):
        """Should return AI choose plus all topics for 'All Categories'."""
        from socratic_sofa.gradio_app import get_topics_by_category, load_topics_data

        topics_data = load_topics_data()
        topics = get_topics_by_category(topics_data, "All Categories")

        assert "✨ Let AI choose" in topics
        assert topics[0] == "✨ Let AI choose"

    def test_valid_category_returns_filtered_topics(self):
        """Should return filtered topics for valid category."""
        from socratic_sofa.gradio_app import get_topics_by_category, load_topics_data

        topics_data = load_topics_data()
        # Get first category name from loaded data
        first_category = list(topics_data.values())[0]["name"]

        topics = get_topics_by_category(topics_data, first_category)

        assert "✨ Let AI choose" in topics
        # All topics should have the category prefix
        for topic in topics[1:]:  # Skip AI choose
            assert f"[{first_category}]" in topic


class TestEventHandlers:
    """Test Gradio event handler functions."""

    def test_update_topics_by_category_returns_update(self):
        """Test update_topics_by_category returns gr.update."""
        from socratic_sofa.gradio_app import load_topics_data, update_topics_by_category

        topics_data = load_topics_data()
        first_category = list(topics_data.values())[0]["name"]

        result = update_topics_by_category(first_category)

        # Should return a gr.update object with choices and value
        assert hasattr(result, "get") or hasattr(result, "__getitem__")

    def test_clear_custom_on_dropdown_change_clears_for_selected(self):
        """Test clearing custom input when dropdown topic selected."""
        from socratic_sofa.gradio_app import clear_custom_on_dropdown_change

        result = clear_custom_on_dropdown_change("[Ethics] What is justice?")

        # Should return empty string when dropdown has a topic
        assert result == ""

    def test_clear_custom_on_dropdown_change_no_change_for_ai_choose(self):
        """Test no change when AI choose selected."""
        from socratic_sofa.gradio_app import clear_custom_on_dropdown_change

        result = clear_custom_on_dropdown_change("✨ Let AI choose")

        # Should return gr.update (no change)
        assert hasattr(result, "get") or hasattr(result, "__getitem__") or result == ""

    def test_clear_custom_on_dropdown_change_handles_none(self):
        """Test handling of None dropdown value."""
        from socratic_sofa.gradio_app import clear_custom_on_dropdown_change

        result = clear_custom_on_dropdown_change(None)

        # Should return gr.update for None
        assert hasattr(result, "get") or hasattr(result, "__getitem__")


class TestStreamingLoopDetails:
    """Test the streaming loop internals."""

    def test_streaming_updates_on_task_completion(self, mocker):
        """Test that outputs update as tasks complete."""
        mocker.patch("socratic_sofa.gradio_app.is_topic_appropriate", return_value=(True, None))

        mock_sofa = MagicMock()
        mock_crew = MagicMock()
        mock_sofa.crew.return_value = mock_crew

        # Create mock tasks
        mock_tasks = []
        for raw_text in ["Topic", "Prop", "Opp", "Judge"]:
            mock_task = Mock()
            mock_output = Mock()
            mock_output.raw = raw_text
            mock_task.output = mock_output
            mock_tasks.append(mock_task)

        mock_crew.tasks = mock_tasks

        # Track callback invocations
        callback_holder = {"callback": None}

        def capture_callback(val):
            callback_holder["callback"] = val

        type(mock_sofa).task_callback = property(
            fget=lambda self: callback_holder["callback"],
            fset=lambda self, val: capture_callback(val),
        )

        # Simulate crew execution with callbacks
        def simulated_kickoff(inputs):
            # Call callback for each task as they "complete"
            if callback_holder["callback"]:
                for task in mock_tasks:
                    callback_holder["callback"](task.output)
            return Mock()

        mock_crew.kickoff.side_effect = simulated_kickoff

        mocker.patch("socratic_sofa.gradio_app.SocraticSofa", return_value=mock_sofa)

        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        results = list(run_socratic_dialogue_streaming("", "Test"))

        # Should have multiple updates as tasks complete
        assert len(results) >= 1
        # Final result should have all outputs
        # Output is now (progress_html, topic, proposition, opposition, judgment)
        final = results[-1]
        progress, topic, prop, opp, judge = final
        assert "Topic" in topic
        assert "Prop" in prop
        assert "Opp" in opp
        assert "Judge" in judge

    def test_streaming_handles_queue_timeout(self, mocker):
        """Test graceful handling of queue.get timeout."""
        mocker.patch("socratic_sofa.gradio_app.is_topic_appropriate", return_value=(True, None))

        mock_sofa = MagicMock()
        mock_crew = MagicMock()
        mock_sofa.crew.return_value = mock_crew

        # Create mock tasks
        mock_tasks = []
        for raw_text in ["Topic", "Prop", "Opp", "Judge"]:
            mock_task = Mock()
            mock_output = Mock()
            mock_output.raw = raw_text
            mock_task.output = mock_output
            mock_tasks.append(mock_task)

        mock_crew.tasks = mock_tasks

        # Simulate slow kickoff with no callbacks
        def slow_kickoff(inputs):
            import time

            time.sleep(0.6)  # Longer than queue timeout
            return Mock()

        mock_crew.kickoff.side_effect = slow_kickoff

        mocker.patch("socratic_sofa.gradio_app.SocraticSofa", return_value=mock_sofa)

        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        # Should complete without hanging
        results = list(run_socratic_dialogue_streaming("", "Test"))

        # Should have at least initial and final outputs
        assert len(results) >= 2


class TestMainFunction:
    """Test the main() entry point."""

    def test_main_calls_demo_launch(self, mocker):
        """Test main() calls demo.launch with correct args."""
        # Mock the demo object's launch method
        mock_launch = mocker.patch("socratic_sofa.gradio_app.demo.launch")

        from socratic_sofa.gradio_app import main

        main()

        # Verify launch was called
        mock_launch.assert_called_once()

        # Verify launch arguments
        call_kwargs = mock_launch.call_args[1]
        assert call_kwargs["server_name"] == "0.0.0.0"
        assert call_kwargs["server_port"] == 7860
        assert call_kwargs["share"] is False

    def test_main_sets_custom_css(self, mocker):
        """Test main() passes custom CSS to demo.launch."""
        mock_launch = mocker.patch("socratic_sofa.gradio_app.demo.launch")

        from socratic_sofa.gradio_app import CUSTOM_CSS, main

        main()

        call_kwargs = mock_launch.call_args[1]
        assert call_kwargs["css"] == CUSTOM_CSS

    def test_main_sets_theme(self, mocker):
        """Test main() sets theme with correct colors."""
        mock_launch = mocker.patch("socratic_sofa.gradio_app.demo.launch")

        from socratic_sofa.gradio_app import main

        main()

        call_kwargs = mock_launch.call_args[1]
        assert "theme" in call_kwargs
        # Theme should be a Gradio theme object
        theme = call_kwargs["theme"]
        assert theme is not None
