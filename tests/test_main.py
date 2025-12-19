"""Tests for main.py CLI entry points.

Tests the CLI functions with mocked CrewAI components.
"""

import json
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest


class TestRunFunction:
    """Test the run() CLI function."""

    @pytest.fixture
    def mock_crew(self, mocker):
        """Mock the SocraticSofa crew."""
        mock_sofa = MagicMock()
        mock_crew_instance = MagicMock()
        mock_result = Mock()
        mock_result.raw = "Test dialogue output"

        mock_crew_instance.kickoff.return_value = mock_result
        mock_sofa.return_value.crew.return_value = mock_crew_instance

        mocker.patch("socratic_sofa.main.SocraticSofa", mock_sofa)
        return mock_sofa, mock_crew_instance, mock_result

    def test_run_calls_kickoff(self, mock_crew):
        """run() should call crew.kickoff with inputs."""
        from socratic_sofa.main import run

        mock_sofa, mock_crew_instance, _ = mock_crew

        run()

        mock_crew_instance.kickoff.assert_called_once()

    def test_run_passes_topic_input(self, mock_crew):
        """run() should pass topic in inputs."""
        from socratic_sofa.main import run

        mock_sofa, mock_crew_instance, _ = mock_crew

        run()

        call_args = mock_crew_instance.kickoff.call_args
        assert "topic" in call_args[1]["inputs"]
        assert call_args[1]["inputs"]["topic"] == "how to enjoy life?"

    def test_run_passes_current_year(self, mock_crew):
        """run() should pass current year in inputs."""
        from datetime import datetime

        from socratic_sofa.main import run

        mock_sofa, mock_crew_instance, _ = mock_crew

        run()

        call_args = mock_crew_instance.kickoff.call_args
        assert "current_year" in call_args[1]["inputs"]
        assert call_args[1]["inputs"]["current_year"] == str(datetime.now().year)

    def test_run_raises_on_exception(self, mock_crew):
        """run() should raise exception with message on error."""
        from socratic_sofa.main import run

        mock_sofa, mock_crew_instance, _ = mock_crew
        mock_crew_instance.kickoff.side_effect = Exception("API Error")

        with pytest.raises(Exception) as exc_info:
            run()

        assert "An error occurred while running the crew" in str(exc_info.value)
        assert "API Error" in str(exc_info.value)


class TestTrainFunction:
    """Test the train() CLI function."""

    @pytest.fixture
    def mock_crew_train(self, mocker):
        """Mock the SocraticSofa crew for training."""
        mock_sofa = MagicMock()
        mock_crew_instance = MagicMock()

        mock_sofa.return_value.crew.return_value = mock_crew_instance
        mocker.patch("socratic_sofa.main.SocraticSofa", mock_sofa)

        return mock_sofa, mock_crew_instance

    def test_train_calls_crew_train(self, mock_crew_train, mocker):
        """train() should call crew.train with arguments."""
        mocker.patch.object(sys, "argv", ["main.py", "5", "output.json"])

        from socratic_sofa.main import train

        mock_sofa, mock_crew_instance = mock_crew_train

        train()

        mock_crew_instance.train.assert_called_once()

    def test_train_passes_iterations(self, mock_crew_train, mocker):
        """train() should pass n_iterations from argv."""
        mocker.patch.object(sys, "argv", ["main.py", "10", "output.json"])

        from socratic_sofa.main import train

        mock_sofa, mock_crew_instance = mock_crew_train

        train()

        call_args = mock_crew_instance.train.call_args
        assert call_args[1]["n_iterations"] == 10

    def test_train_passes_filename(self, mock_crew_train, mocker):
        """train() should pass filename from argv."""
        mocker.patch.object(sys, "argv", ["main.py", "5", "training_output.json"])

        from socratic_sofa.main import train

        mock_sofa, mock_crew_instance = mock_crew_train

        train()

        call_args = mock_crew_instance.train.call_args
        assert call_args[1]["filename"] == "training_output.json"

    def test_train_raises_on_exception(self, mock_crew_train, mocker):
        """train() should raise exception with message on error."""
        mocker.patch.object(sys, "argv", ["main.py", "5", "output.json"])

        from socratic_sofa.main import train

        mock_sofa, mock_crew_instance = mock_crew_train
        mock_crew_instance.train.side_effect = Exception("Training Error")

        with pytest.raises(Exception) as exc_info:
            train()

        assert "An error occurred while training the crew" in str(exc_info.value)


class TestReplayFunction:
    """Test the replay() CLI function."""

    @pytest.fixture
    def mock_crew_replay(self, mocker):
        """Mock the SocraticSofa crew for replay."""
        mock_sofa = MagicMock()
        mock_crew_instance = MagicMock()

        mock_sofa.return_value.crew.return_value = mock_crew_instance
        mocker.patch("socratic_sofa.main.SocraticSofa", mock_sofa)

        return mock_sofa, mock_crew_instance

    def test_replay_calls_crew_replay(self, mock_crew_replay, mocker):
        """replay() should call crew.replay with task_id."""
        mocker.patch.object(sys, "argv", ["main.py", "task-123"])

        from socratic_sofa.main import replay

        mock_sofa, mock_crew_instance = mock_crew_replay

        replay()

        mock_crew_instance.replay.assert_called_once_with(task_id="task-123")

    def test_replay_raises_on_exception(self, mock_crew_replay, mocker):
        """replay() should raise exception with message on error."""
        mocker.patch.object(sys, "argv", ["main.py", "task-123"])

        from socratic_sofa.main import replay

        mock_sofa, mock_crew_instance = mock_crew_replay
        mock_crew_instance.replay.side_effect = Exception("Replay Error")

        with pytest.raises(Exception) as exc_info:
            replay()

        assert "An error occurred while replaying the crew" in str(exc_info.value)


class TestTestFunction:
    """Test the test() CLI function."""

    @pytest.fixture
    def mock_crew_test(self, mocker):
        """Mock the SocraticSofa crew for testing."""
        mock_sofa = MagicMock()
        mock_crew_instance = MagicMock()

        mock_sofa.return_value.crew.return_value = mock_crew_instance
        mocker.patch("socratic_sofa.main.SocraticSofa", mock_sofa)

        return mock_sofa, mock_crew_instance

    def test_test_calls_crew_test(self, mock_crew_test, mocker):
        """test() should call crew.test with arguments."""
        mocker.patch.object(sys, "argv", ["main.py", "3", "gpt-4"])

        from socratic_sofa.main import test

        mock_sofa, mock_crew_instance = mock_crew_test

        test()

        mock_crew_instance.test.assert_called_once()

    def test_test_passes_iterations(self, mock_crew_test, mocker):
        """test() should pass n_iterations from argv."""
        mocker.patch.object(sys, "argv", ["main.py", "5", "gpt-4"])

        from socratic_sofa.main import test

        mock_sofa, mock_crew_instance = mock_crew_test

        test()

        call_args = mock_crew_instance.test.call_args
        assert call_args[1]["n_iterations"] == 5

    def test_test_passes_eval_llm(self, mock_crew_test, mocker):
        """test() should pass eval_llm from argv."""
        mocker.patch.object(sys, "argv", ["main.py", "3", "claude-3"])

        from socratic_sofa.main import test

        mock_sofa, mock_crew_instance = mock_crew_test

        test()

        call_args = mock_crew_instance.test.call_args
        assert call_args[1]["eval_llm"] == "claude-3"

    def test_test_raises_on_exception(self, mock_crew_test, mocker):
        """test() should raise exception with message on error."""
        mocker.patch.object(sys, "argv", ["main.py", "3", "gpt-4"])

        from socratic_sofa.main import test

        mock_sofa, mock_crew_instance = mock_crew_test
        mock_crew_instance.test.side_effect = Exception("Test Error")

        with pytest.raises(Exception) as exc_info:
            test()

        assert "An error occurred while testing the crew" in str(exc_info.value)


class TestRunWithTriggerFunction:
    """Test the run_with_trigger() CLI function."""

    @pytest.fixture
    def mock_crew_trigger(self, mocker):
        """Mock the SocraticSofa crew for trigger runs."""
        mock_sofa = MagicMock()
        mock_crew_instance = MagicMock()
        mock_result = Mock()
        mock_result.raw = "Trigger output"

        mock_crew_instance.kickoff.return_value = mock_result
        mock_sofa.return_value.crew.return_value = mock_crew_instance

        mocker.patch("socratic_sofa.main.SocraticSofa", mock_sofa)
        return mock_sofa, mock_crew_instance, mock_result

    def test_run_with_trigger_parses_json_payload(self, mock_crew_trigger, mocker):
        """run_with_trigger() should parse JSON payload from argv."""
        payload = {"topic": "test topic", "extra": "data"}
        mocker.patch.object(sys, "argv", ["main.py", json.dumps(payload)])

        from socratic_sofa.main import run_with_trigger

        mock_sofa, mock_crew_instance, _ = mock_crew_trigger

        run_with_trigger()

        call_args = mock_crew_instance.kickoff.call_args
        assert call_args[1]["inputs"]["crewai_trigger_payload"] == payload

    def test_run_with_trigger_raises_on_missing_payload(self, mock_crew_trigger, mocker):
        """run_with_trigger() should raise when no payload provided."""
        mocker.patch.object(sys, "argv", ["main.py"])

        from socratic_sofa.main import run_with_trigger

        with pytest.raises(Exception) as exc_info:
            run_with_trigger()

        assert "No trigger payload provided" in str(exc_info.value)

    def test_run_with_trigger_raises_on_invalid_json(self, mock_crew_trigger, mocker):
        """run_with_trigger() should raise on invalid JSON."""
        mocker.patch.object(sys, "argv", ["main.py", "not valid json"])

        from socratic_sofa.main import run_with_trigger

        with pytest.raises(Exception) as exc_info:
            run_with_trigger()

        assert "Invalid JSON payload" in str(exc_info.value)

    def test_run_with_trigger_raises_on_crew_error(self, mock_crew_trigger, mocker):
        """run_with_trigger() should raise on crew execution error."""
        payload = {"topic": "test"}
        mocker.patch.object(sys, "argv", ["main.py", json.dumps(payload)])

        from socratic_sofa.main import run_with_trigger

        mock_sofa, mock_crew_instance, _ = mock_crew_trigger
        mock_crew_instance.kickoff.side_effect = Exception("Trigger Error")

        with pytest.raises(Exception) as exc_info:
            run_with_trigger()

        assert "An error occurred while running the crew with trigger" in str(
            exc_info.value
        )

    def test_run_with_trigger_returns_result(self, mock_crew_trigger, mocker):
        """run_with_trigger() should return the crew result."""
        payload = {"topic": "test"}
        mocker.patch.object(sys, "argv", ["main.py", json.dumps(payload)])

        from socratic_sofa.main import run_with_trigger

        mock_sofa, mock_crew_instance, mock_result = mock_crew_trigger

        result = run_with_trigger()

        assert result == mock_result
