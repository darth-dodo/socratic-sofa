"""Tests for gradio_app.py streaming functionality.

Tests the run_socratic_dialogue_streaming generator function with mocked
CrewAI components to avoid API calls.
"""

from queue import Queue
from threading import Thread
from unittest.mock import MagicMock, Mock, patch

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
        mocker.patch(
            "socratic_sofa.gradio_app.is_topic_appropriate", return_value=(True, None)
        )

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
        error_msg = results[0][0]
        assert "⚠️" in error_msg
        assert "Topic is inappropriate" in error_msg
        assert "Suggested topics:" in error_msg
        assert "What is justice?" in error_msg

    def test_inappropriate_topic_all_outputs_same_error(
        self, mock_content_filter_inappropriate
    ):
        """All four outputs should contain the same error message."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        results = list(run_socratic_dialogue_streaming("", "bad topic"))

        assert len(results) == 1
        topic, prop, opp, judge = results[0]
        assert topic == prop == opp == judge

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

        assert "⏳" in first_result[0]
        assert "Preparing philosophical inquiry" in first_result[0]

    def test_handles_crew_exception(
        self, mock_crew_components, mock_content_filter_appropriate
    ):
        """Should yield error message when crew raises exception."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        mock_sofa, mock_crew, _ = mock_crew_components
        mock_crew.kickoff.side_effect = Exception("API Error")

        results = list(run_socratic_dialogue_streaming("", "What is truth?"))

        # Should have at least the initial loading state and error
        final_result = results[-1]
        assert "❌" in final_result[0]
        assert "Error running dialogue" in final_result[0]

    def test_final_output_uses_task_outputs(
        self, mock_crew_components, mock_content_filter_appropriate
    ):
        """Should use task outputs for final yield."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        mock_sofa, mock_crew, mock_outputs = mock_crew_components

        results = list(run_socratic_dialogue_streaming("", "What is truth?"))

        final_result = results[-1]
        assert "Topic output" in final_result[0]
        assert "Proposition output" in final_result[1]
        assert "Opposition output" in final_result[2]
        assert "Judgment output" in final_result[3]

    def test_proposition_has_header(
        self, mock_crew_components, mock_content_filter_appropriate
    ):
        """Proposition output should include header."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        results = list(run_socratic_dialogue_streaming("", "What is truth?"))

        final_result = results[-1]
        assert "## 🔵 First Line of Inquiry" in final_result[1]

    def test_opposition_has_header(
        self, mock_crew_components, mock_content_filter_appropriate
    ):
        """Opposition output should include header."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        results = list(run_socratic_dialogue_streaming("", "What is truth?"))

        final_result = results[-1]
        assert "## 🟢 Alternative Line of Inquiry" in final_result[2]

    def test_uses_custom_topic_over_dropdown(
        self, mock_crew_components, mock_content_filter_appropriate, mocker
    ):
        """Custom topic should take priority over dropdown."""
        from socratic_sofa.gradio_app import run_socratic_dialogue_streaming

        mock_sofa, mock_crew, _ = mock_crew_components

        list(
            run_socratic_dialogue_streaming(
                "[Category] Dropdown Topic", "Custom Topic"
            )
        )

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
        mocker.patch(
            "socratic_sofa.gradio_app.is_topic_appropriate", return_value=(True, None)
        )

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
        mocker.patch(
            "socratic_sofa.gradio_app.is_topic_appropriate", return_value=(True, None)
        )

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
        mocker.patch(
            "socratic_sofa.gradio_app.is_topic_appropriate", return_value=(True, None)
        )

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
        final = results[-1]
        assert "Topic" in final[0]
        assert "Opp" in final[2]


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
