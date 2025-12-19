"""Unit tests for SocraticSofa crew class structure.

Tests focus on class structure and type annotations without
requiring API keys or executing the crew.
"""

import pytest

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
        assert "Callable" in callback_annotation or "collections.abc.Callable" in callback_annotation

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
