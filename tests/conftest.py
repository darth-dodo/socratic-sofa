"""Pytest configuration and shared fixtures for Socratic Sofa tests.

This module provides common fixtures and configuration for all tests.
"""

import os
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the project root directory.

    Returns:
        Path to the project root directory
    """
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def src_root(project_root: Path) -> Path:
    """Return the source code root directory.

    Args:
        project_root: Project root directory fixture

    Returns:
        Path to the src/socratic_sofa directory
    """
    return project_root / "src" / "socratic_sofa"


@pytest.fixture(scope="session")
def config_dir(src_root: Path) -> Path:
    """Return the config directory.

    Args:
        src_root: Source root directory fixture

    Returns:
        Path to the config directory
    """
    return src_root / "config"


@pytest.fixture(scope="session")
def outputs_dir(project_root: Path) -> Path:
    """Return the outputs directory.

    Args:
        project_root: Project root directory fixture

    Returns:
        Path to the outputs directory
    """
    return project_root / "outputs"


@pytest.fixture
def mock_api_key(monkeypatch: pytest.MonkeyPatch) -> Generator[str, None, None]:
    """Provide a mock Anthropic API key for testing.

    Args:
        monkeypatch: Pytest monkeypatch fixture

    Yields:
        Mock API key string
    """
    mock_key = "sk-ant-test-mock-api-key-for-testing-only"
    monkeypatch.setenv("ANTHROPIC_API_KEY", mock_key)
    yield mock_key
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)


@pytest.fixture
def sample_topic() -> str:
    """Provide a sample philosophical topic for testing.

    Returns:
        Sample topic string
    """
    return "What is justice?"


@pytest.fixture
def sample_inquiry() -> str:
    """Provide a sample Socratic inquiry for testing.

    Returns:
        Sample inquiry string
    """
    return "Is justice giving each person what they deserve?"


@pytest.fixture
def sample_response() -> str:
    """Provide a sample response for testing.

    Returns:
        Sample response string
    """
    return "Yes, justice means giving people what they have earned through their actions."


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Provide a temporary directory for test outputs.

    Args:
        tmp_path: Pytest temporary path fixture

    Returns:
        Path to temporary outputs directory
    """
    output_path = tmp_path / "outputs"
    output_path.mkdir(exist_ok=True)
    return output_path


@pytest.fixture(autouse=True)
def reset_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reset environment variables before each test.

    This ensures test isolation by preventing environment variable leakage.

    Args:
        monkeypatch: Pytest monkeypatch fixture
    """
    # Store original values
    original_api_key = os.getenv("ANTHROPIC_API_KEY")

    yield

    # Restore original values after test
    if original_api_key:
        monkeypatch.setenv("ANTHROPIC_API_KEY", original_api_key)
    else:
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
