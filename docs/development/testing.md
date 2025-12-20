# Testing Guide

Comprehensive testing guide for Socratic Sofa development.

## Table of Contents

- [Overview](#overview)
- [Test Suite Structure](#test-suite-structure)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Test Fixtures](#test-fixtures)
- [Writing Tests](#writing-tests)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Best Practices](#best-practices)

## Overview

Socratic Sofa has a comprehensive test suite with **220+ tests** covering all major modules. The tests are designed to run without requiring actual API keys by using mocks and fixtures.

### Testing Stack

- **pytest**: Test framework
- **pytest-mock**: Mocking utilities
- **pytest-cov**: Coverage reporting
- **pre-commit**: Automated quality checks on commit

### Test Categories

| Category       | Description                               | Count     |
| -------------- | ----------------------------------------- | --------- |
| Content Filter | Topic validation, moderation, suggestions | 43 tests  |
| Crew           | CrewAI structure, agents, tasks           | 27 tests  |
| Gradio App     | Web interface, topic handling, streaming  | 50+ tests |
| Logging        | Structured logging, formatters, adapters  | 20 tests  |
| Rate Limiter   | Rate limiting decorators                  | 13 tests  |
| Edge Cases     | Boundary conditions across all modules    | 26 tests  |
| Main           | CLI entry points                          | 15 tests  |

## Test Suite Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_content_filter.py   # Content moderation tests
├── test_crew.py             # CrewAI crew structure tests
├── test_edge_cases.py       # Edge cases across all modules
├── test_gradio_app.py       # Web interface tests
├── test_gradio_app_streaming.py  # Streaming functionality tests
├── test_logging_config.py   # Structured logging tests
├── test_main.py             # CLI entry point tests
└── test_rate_limiter.py     # Rate limiting tests
```

## Running Tests

### Basic Commands

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage report
uv run pytest tests/ --cov=src/socratic_sofa --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_content_filter.py -v

# Run specific test class
uv run pytest tests/test_crew.py::TestSocraticSofaStructure -v

# Run specific test
uv run pytest tests/test_crew.py::TestSocraticSofaStructure::test_class_exists -v

# Run tests matching a pattern
uv run pytest -k "topic" -v

# Run with short traceback
uv run pytest tests/ -v --tb=short
```

### Makefile Commands

```bash
# Run all tests
make test

# Run with coverage
make test-cov
```

### Test Output

```
============================= test session starts ==============================
platform darwin -- Python 3.12.11, pytest-9.0.2, pluggy-1.6.0
plugins: mock-3.15.1, anyio-4.12.0, cov-7.0.0
collected 220 items

tests/test_content_filter.py ......................................... [ 19%]
tests/test_crew.py ..........................                           [ 31%]
tests/test_edge_cases.py ..........................                     [ 43%]
tests/test_gradio_app.py ...................................            [ 58%]
tests/test_gradio_app_streaming.py ..........................           [ 70%]
tests/test_logging_config.py ....................                       [ 79%]
tests/test_main.py ...............                                      [ 86%]
tests/test_rate_limiter.py .............                                [100%]

======================= 220 passed in 125.02s (0:02:05) ========================
```

## Test Coverage

Current test coverage is approximately **99%** across all modules.

### Generate Coverage Report

```bash
# Terminal report with missing lines
uv run pytest --cov=src/socratic_sofa --cov-report=term-missing

# HTML report
uv run pytest --cov=src/socratic_sofa --cov-report=html
open htmlcov/index.html

# XML report (for CI)
uv run pytest --cov=src/socratic_sofa --cov-report=xml
```

### Coverage by Module

| Module            | Coverage |
| ----------------- | -------- |
| content_filter.py | 100%     |
| crew.py           | 99%      |
| gradio_app.py     | 99%      |
| logging_config.py | 100%     |
| rate_limiter.py   | 100%     |
| main.py           | 100%     |

## Test Fixtures

### Shared Fixtures (conftest.py)

The `conftest.py` file provides common fixtures used across all tests:

```python
# Mock API keys (autouse - applies to all tests)
@pytest.fixture(autouse=True)
def mock_openai_api_key(monkeypatch):
    """Provide mock OpenAI API key for CrewAI tests."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-mock-key")

# Sample data fixtures
@pytest.fixture
def sample_topic():
    """Provide a sample philosophical topic."""
    return "What is justice?"

# Path fixtures
@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent
```

### Key Fixtures

| Fixture               | Scope              | Description                    |
| --------------------- | ------------------ | ------------------------------ |
| `mock_openai_api_key` | function (autouse) | Prevents CrewAI API key errors |
| `mock_api_key`        | function           | Mock Anthropic API key         |
| `sample_topic`        | function           | Sample philosophical topic     |
| `project_root`        | session            | Project root path              |
| `src_root`            | session            | Source code path               |
| `config_dir`          | session            | Config directory path          |

## Writing Tests

### Unit Test Example

```python
# tests/test_content_filter.py
import pytest
from socratic_sofa.content_filter import is_topic_appropriate

class TestIsTopicAppropriate:
    """Tests for is_topic_appropriate function."""

    def test_empty_topic_returns_appropriate(self, mocker):
        """Empty string should be accepted without API call."""
        mock_client = mocker.patch("socratic_sofa.content_filter.Anthropic")
        is_appropriate, reason = is_topic_appropriate("")
        assert is_appropriate is True
        assert reason == ""
        mock_client.assert_not_called()

    def test_topic_over_500_chars_returns_inappropriate(self, mocker):
        """Topics over 500 characters should be rejected."""
        mock_client = mocker.patch("socratic_sofa.content_filter.Anthropic")
        topic = "a" * 501
        is_appropriate, reason = is_topic_appropriate(topic)
        assert is_appropriate is False
        assert "too long" in reason.lower()
        mock_client.assert_not_called()
```

### Mocking External Services

```python
def test_appropriate_response_returns_true(self, mocker):
    """Test that APPROPRIATE response returns True."""
    mock_response = mocker.MagicMock()
    mock_response.content = [mocker.MagicMock(text="APPROPRIATE")]

    mock_client = mocker.patch("socratic_sofa.content_filter.Anthropic")
    mock_client.return_value.messages.create.return_value = mock_response

    is_appropriate, reason = is_topic_appropriate("What is justice?")

    assert is_appropriate is True
    assert reason == ""
```

### Testing Decorators

```python
def test_rate_limited_allows_calls_under_limit(self):
    """Test that calls under limit are allowed."""
    from socratic_sofa.rate_limiter import rate_limited

    call_count = 0

    @rate_limited(calls=5, period=60)
    def test_func():
        nonlocal call_count
        call_count += 1
        return "success"

    # Should allow 5 calls
    for _ in range(5):
        result = test_func()
        assert result == "success"

    assert call_count == 5
```

### Testing Logging

```python
def test_logs_start_message(self, caplog):
    """Test that log_timing logs start message."""
    from socratic_sofa.logging_config import get_logger, log_timing

    logger = get_logger("test")

    with caplog.at_level(logging.DEBUG):
        with log_timing(logger, "test_operation"):
            pass

    assert "Starting test_operation" in caplog.text
```

## Pre-commit Hooks

Pre-commit hooks run automatically on every commit to catch issues early.

### Installation

```bash
# Install hooks
.venv/bin/pre-commit install
.venv/bin/pre-commit install --hook-type commit-msg
```

### Manual Execution

```bash
# Run on all files
.venv/bin/pre-commit run --all-files

# Run specific hook
.venv/bin/pre-commit run ruff --all-files
```

### Configured Hooks

| Hook                    | Description              |
| ----------------------- | ------------------------ |
| isort                   | Import sorting           |
| ruff                    | Linting and auto-fix     |
| ruff-format             | Code formatting          |
| bandit                  | Security scanning        |
| detect-secrets          | Secret detection         |
| vulture                 | Dead code detection      |
| prettier                | Markdown/YAML formatting |
| conventional-pre-commit | Commit message format    |

### Example Pre-commit Output

```
isort....................................................................Passed
ruff.....................................................................Passed
ruff-format..............................................................Passed
bandit...................................................................Passed
Detect secrets...........................................................Passed
vulture..................................................................Passed
prettier.................................................................Passed
Conventional Commit......................................................Passed
```

## Best Practices

### Test Organization

1. **One test class per logical group**: Group related tests together
2. **Descriptive test names**: `test_empty_topic_returns_appropriate`
3. **Arrange-Act-Assert pattern**: Clear test structure

### Mocking Guidelines

1. **Mock at the boundary**: Mock external services, not internal logic
2. **Use mocker fixture**: pytest-mock provides cleaner syntax
3. **Verify mock calls**: Assert that mocks were called correctly

### Edge Cases to Test

- Empty strings and None values
- Boundary conditions (e.g., exactly 500 chars)
- Unicode and special characters
- Error conditions and exceptions
- Concurrent access patterns

### Testing AI Components

1. **Mock API calls**: Don't make real API calls in tests
2. **Test structure, not content**: Verify output format, not AI responses
3. **Test configuration**: Verify agents/tasks are configured correctly
4. **Test error handling**: Verify graceful degradation

### CI/CD Integration

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: uv run pytest tests/ -v --cov=src/socratic_sofa
  env:
    OPENAI_API_KEY: "mock-key"
    ANTHROPIC_API_KEY: "mock-key"
```

## Troubleshooting

### Common Issues

**CrewAI API Key Error**:

```
ImportError: OPENAI_API_KEY is required
```

Solution: The `mock_openai_api_key` fixture in `conftest.py` should handle this automatically. If not, ensure conftest.py is in the tests directory.

**Slow Tests**:
Use `-x` flag to stop on first failure:

```bash
uv run pytest tests/ -x -v
```

**Debugging Tests**:
Use `-s` to see print output:

```bash
uv run pytest tests/test_content_filter.py -v -s
```

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [pre-commit Documentation](https://pre-commit.com/)
