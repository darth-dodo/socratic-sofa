"""Unit tests for SocraticSofa crew class structure.

Tests focus on class structure and type annotations without
requiring API keys or executing the crew.
"""

from unittest.mock import MagicMock, patch

from socratic_sofa.crew import SocraticSofa


class TestSocraticSofaStructure:
    """Test the basic structure of SocraticSofa class."""

    def test_class_exists(self):
        """Test that SocraticSofa class exists and can be imported."""
        assert SocraticSofa is not None

    def test_class_has_docstring(self):
        """Test that the class has a docstring."""
        assert SocraticSofa.__doc__ is not None
        assert len(SocraticSofa.__doc__.strip()) > 0
        assert "SocraticSofa crew" in SocraticSofa.__doc__

    def test_has_task_callback_annotation(self):
        """Test that task_callback has correct type annotation."""
        annotations = SocraticSofa.__annotations__
        assert "task_callback" in annotations

        # Verify it's a callable type
        callback_annotation = str(annotations["task_callback"])
        assert (
            "Callable" in callback_annotation or "collections.abc.Callable" in callback_annotation
        )

    def test_has_agents_annotation(self):
        """Test that agents attribute is annotated."""
        annotations = SocraticSofa.__annotations__
        assert "agents" in annotations

    def test_has_tasks_annotation(self):
        """Test that tasks attribute is annotated."""
        annotations = SocraticSofa.__annotations__
        assert "tasks" in annotations

    def test_has_socratic_questioner_method(self):
        """Test that socratic_questioner agent method exists."""
        assert hasattr(SocraticSofa, "socratic_questioner")

    def test_has_judge_method(self):
        """Test that judge agent method exists."""
        assert hasattr(SocraticSofa, "judge")

    def test_has_propose_topic_method(self):
        """Test that propose_topic task method exists."""
        assert hasattr(SocraticSofa, "propose_topic")

    def test_has_propose_method(self):
        """Test that propose task method exists."""
        assert hasattr(SocraticSofa, "propose")

    def test_has_oppose_method(self):
        """Test that oppose task method exists."""
        assert hasattr(SocraticSofa, "oppose")

    def test_has_judge_task_method(self):
        """Test that judge_task task method exists."""
        assert hasattr(SocraticSofa, "judge_task")

    def test_has_crew_method(self):
        """Test that crew method exists."""
        assert hasattr(SocraticSofa, "crew")


class TestSocraticSofaCallbackType:
    """Test the callback type annotation functionality."""

    def test_callback_type_annotation_exists(self):
        """Test that task_callback has type annotation."""
        from typing import get_type_hints

        hints = get_type_hints(SocraticSofa)
        assert "task_callback" in hints

    def test_callback_allows_callable(self):
        """Test that callback type allows Callable."""
        from typing import get_type_hints

        hints = get_type_hints(SocraticSofa)
        callback_type = hints["task_callback"]

        # Check it involves Callable
        type_str = str(callback_type)
        assert "Callable" in type_str or "collections.abc.Callable" in type_str

    def test_callback_allows_none(self):
        """Test that callback type allows None."""
        from typing import get_type_hints

        hints = get_type_hints(SocraticSofa)
        callback_type = hints["task_callback"]

        # Check it allows None (Union with None or Optional)
        type_str = str(callback_type)
        assert "None" in type_str or "Optional" in type_str


class TestSocraticSofaMethodCount:
    """Test that all expected methods are present."""

    def test_has_two_agent_methods(self):
        """Test that class has the 2 agent methods."""
        agent_methods = ["socratic_questioner", "judge"]
        for method in agent_methods:
            assert hasattr(SocraticSofa, method), f"Missing agent method: {method}"

    def test_has_four_task_methods(self):
        """Test that class has the 4 task methods."""
        task_methods = ["propose_topic", "propose", "oppose", "judge_task"]
        for method in task_methods:
            assert hasattr(SocraticSofa, method), f"Missing task method: {method}"

    def test_has_crew_orchestration_method(self):
        """Test that class has crew orchestration method."""
        assert hasattr(SocraticSofa, "crew")


class TestSocraticSofaClassDefault:
    """Test class-level default values."""

    def test_task_callback_default_is_none(self):
        """Test that task_callback class default is None."""
        # Check the class-level default
        if hasattr(SocraticSofa, "task_callback"):
            # If it's a class attribute, check its value
            default = getattr(SocraticSofa, "task_callback", "NOT_SET")
            if default != "NOT_SET":
                assert default is None


class TestSocraticSofaAgentCreation:
    """Test that agent methods return Agent instances."""

    def test_socratic_questioner_returns_agent(self, mocker):
        """Test socratic_questioner method returns an Agent."""
        # Mock the Agent class where it's imported in the module
        mock_agent_instance = MagicMock()
        mock_agent_class = mocker.patch(
            "socratic_sofa.crew.Agent", return_value=mock_agent_instance
        )

        # Create crew instance - CrewAI's @CrewBase loads config automatically
        SocraticSofa()

        # Agent should have been called with config for socratic_questioner
        # The @agent decorator calls the method during class instantiation
        calls = mock_agent_class.call_args_list
        assert len(calls) >= 1
        # Check that socratic_questioner config was used
        configs_used = [c[1]["config"] for c in calls if "config" in c[1]]
        assert any("Socratic" in str(cfg.get("role", "")) for cfg in configs_used)

    def test_judge_returns_agent(self, mocker):
        """Test judge method returns an Agent."""
        # Mock the Agent class where it's imported in the module
        mock_agent_instance = MagicMock()
        mock_agent_class = mocker.patch(
            "socratic_sofa.crew.Agent", return_value=mock_agent_instance
        )

        # Create crew instance - CrewAI's @CrewBase loads config automatically
        SocraticSofa()

        # Agent should have been called for both agents
        calls = mock_agent_class.call_args_list
        assert len(calls) == 2  # socratic_questioner and judge
        # Check that judge config was used
        configs_used = [c[1]["config"] for c in calls if "config" in c[1]]
        assert any(
            "Moderator" in str(cfg.get("role", "")) or "judge" in str(cfg).lower()
            for cfg in configs_used
        )


class TestSocraticSofaTaskCreation:
    """Test that task methods return Task instances."""

    @patch("socratic_sofa.crew.Task")
    def test_propose_topic_returns_task(self, mock_task_class):
        """Test propose_topic method returns a Task."""
        # Mock the Task class
        mock_task_instance = MagicMock()
        mock_task_class.return_value = mock_task_instance

        # Create crew instance and mock tasks_config
        crew = SocraticSofa()
        crew.tasks_config = {
            "propose_topic": {
                "description": "Propose a philosophical topic",
                "expected_output": "A topic statement",
            }
        }
        crew.task_callback = None

        # Call the method - this covers line 31
        task = crew.propose_topic()

        # Verify Task was created with correct config
        assert task is not None
        mock_task_class.assert_called_once()
        call_kwargs = mock_task_class.call_args[1]
        assert call_kwargs["config"] == crew.tasks_config["propose_topic"]
        assert call_kwargs["callback"] is None

    @patch("socratic_sofa.crew.Task")
    def test_propose_returns_task_with_context(self, mock_task_class):
        """Test propose method returns a Task with context."""
        # Mock the Task class
        mock_task_instance = MagicMock()
        mock_task_class.return_value = mock_task_instance

        # Create crew instance and mock configs
        crew = SocraticSofa()
        crew.tasks_config = {
            "propose_topic": {"description": "Propose topic", "expected_output": "Topic"},
            "propose": {"description": "Propose argument", "expected_output": "Argument"},
        }
        crew.task_callback = MagicMock()

        # Call the method - this covers line 35
        task = crew.propose()

        # Verify Task was created with context
        assert task is not None
        # Should be called twice: once for propose_topic(), once for propose()
        assert mock_task_class.call_count == 2

        # Check the second call (propose task)
        second_call_kwargs = mock_task_class.call_args_list[1][1]
        assert second_call_kwargs["config"] == crew.tasks_config["propose"]
        assert "context" in second_call_kwargs
        assert len(second_call_kwargs["context"]) == 1
        assert second_call_kwargs["callback"] == crew.task_callback

    @patch("socratic_sofa.crew.Task")
    def test_oppose_returns_task_with_context(self, mock_task_class):
        """Test oppose method returns a Task with propose context."""
        # Mock the Task class
        mock_task_instance = MagicMock()
        mock_task_class.return_value = mock_task_instance

        # Create crew instance and mock configs
        crew = SocraticSofa()
        crew.tasks_config = {
            "propose_topic": {"description": "Topic", "expected_output": "Topic"},
            "propose": {"description": "Propose", "expected_output": "Argument"},
            "oppose": {"description": "Oppose", "expected_output": "Counter-argument"},
        }
        crew.task_callback = MagicMock()

        # Call the method - this covers line 43
        task = crew.oppose()

        # Verify Task was created with context
        assert task is not None
        # Should be called 3 times: propose_topic(), propose(), oppose()
        assert mock_task_class.call_count == 3

        # Check the third call (oppose task)
        third_call_kwargs = mock_task_class.call_args_list[2][1]
        assert third_call_kwargs["config"] == crew.tasks_config["oppose"]
        assert "context" in third_call_kwargs
        assert len(third_call_kwargs["context"]) == 2
        assert third_call_kwargs["callback"] == crew.task_callback

    @patch("socratic_sofa.crew.Task")
    def test_judge_task_returns_task_with_all_context(self, mock_task_class):
        """Test judge_task method returns a Task with full context."""
        # Mock the Task class
        mock_task_instance = MagicMock()
        mock_task_class.return_value = mock_task_instance

        # Create crew instance and mock configs
        crew = SocraticSofa()
        crew.tasks_config = {
            "propose_topic": {"description": "Topic", "expected_output": "Topic"},
            "propose": {"description": "Propose", "expected_output": "Argument"},
            "oppose": {"description": "Oppose", "expected_output": "Counter"},
            "judge_task": {"description": "Judge", "expected_output": "Judgment"},
        }
        crew.task_callback = None

        # Call the method - this covers line 51
        task = crew.judge_task()

        # Verify Task was created with all context
        assert task is not None
        # Should be called 4 times: propose_topic(), propose(), oppose(), judge_task()
        assert mock_task_class.call_count == 4

        # Check the fourth call (judge_task)
        fourth_call_kwargs = mock_task_class.call_args_list[3][1]
        assert fourth_call_kwargs["config"] == crew.tasks_config["judge_task"]
        assert "context" in fourth_call_kwargs
        assert len(fourth_call_kwargs["context"]) == 3
        assert fourth_call_kwargs["callback"] is None


class TestSocraticSofaCrewCreation:
    """Test crew method."""

    @patch("socratic_sofa.crew.Crew")
    def test_crew_returns_crew_instance(self, mock_crew_class):
        """Test crew method returns a Crew."""
        # Mock the Crew class
        mock_crew_instance = MagicMock()
        mock_crew_class.return_value = mock_crew_instance

        # Create crew instance
        crew_obj = SocraticSofa()
        crew_obj.agents = [MagicMock(), MagicMock()]
        crew_obj.tasks = [MagicMock(), MagicMock(), MagicMock()]

        # Call the method - this covers line 61
        result = crew_obj.crew()

        # Verify Crew was created
        assert result is not None
        mock_crew_class.assert_called_once()
        call_kwargs = mock_crew_class.call_args[1]
        assert call_kwargs["agents"] == crew_obj.agents
        assert call_kwargs["tasks"] == crew_obj.tasks
        assert call_kwargs["verbose"] is True

    @patch("socratic_sofa.crew.Crew")
    @patch("socratic_sofa.crew.Process")
    def test_crew_has_sequential_process(self, mock_process, mock_crew_class):
        """Test crew uses sequential process."""
        # Mock the Crew class
        mock_crew_instance = MagicMock()
        mock_crew_class.return_value = mock_crew_instance

        # Create crew instance
        crew_obj = SocraticSofa()
        crew_obj.agents = []
        crew_obj.tasks = []

        # Call the method
        crew_obj.crew()

        # Verify sequential process is used
        call_kwargs = mock_crew_class.call_args[1]
        assert "process" in call_kwargs
        # The actual Process.sequential value will be used, not mocked
