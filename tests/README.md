# Socratic Sofa Test Suite

This directory contains the test infrastructure for the Socratic Sofa project.

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared pytest fixtures and configuration
├── test_content_filter.py   # Content filtering tests (placeholder)
├── test_crew.py             # CrewAI crew coordination tests (placeholder)
└── test_gradio_app.py       # Gradio web interface tests (placeholder)
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
make test

# Run with coverage report
make test-cov

# Run specific test file
uv run --extra test pytest tests/test_crew.py

# Run with verbose output
uv run --extra test pytest -vv
```

### Coverage Reports

```bash
# Terminal coverage report
make test-cov

# Generate HTML coverage report
uv run --extra test pytest --cov=src/socratic_sofa --cov-report=html

# View HTML report (opens in browser)
open htmlcov/index.html
```

## Available Fixtures

The `conftest.py` module provides the following shared fixtures:

### Path Fixtures

- `project_root` - Path to the project root directory
- `src_root` - Path to the src/socratic_sofa directory
- `config_dir` - Path to the config directory
- `outputs_dir` - Path to the outputs directory
- `temp_output_dir` - Temporary directory for test outputs

### Mock Fixtures

- `mock_api_key` - Mock Anthropic API key for testing

### Sample Data Fixtures

- `sample_topic` - Sample philosophical topic
- `sample_inquiry` - Sample Socratic inquiry
- `sample_response` - Sample response

### Environment Fixtures

- `reset_env_vars` - Auto-used fixture for environment isolation

## Test Categories

### Content Filter Tests (`test_content_filter.py`)

**Purpose**: Validate content safety and filtering mechanisms

**Planned Tests**:

- Inappropriate content detection
- Offensive language filtering
- Harmful content blocking
- Edge cases and boundary conditions
- Filter configuration and customization

### Crew Tests (`test_crew.py`)

**Purpose**: Validate CrewAI crew coordination and agent interactions

**Planned Tests**:

- Crew initialization and configuration
- Agent creation and setup
- Task execution flow
- Dialogue progression through stages
- Crew kickoff and result handling
- Error handling and recovery

### Gradio App Tests (`test_gradio_app.py`)

**Purpose**: Validate web interface functionality

**Planned Tests**:

- Interface initialization
- User input processing
- Dialogue state management
- UI component rendering
- Error display and handling
- Example loading functionality

## Testing Best Practices

### Test Organization

1. **One test class per component** - Group related tests in classes
2. **Clear test names** - Use descriptive names that explain what's being tested
3. **Arrange-Act-Assert pattern** - Structure tests with clear setup, execution, and verification

### Fixtures Usage

```python
def test_with_fixtures(sample_topic, mock_api_key, temp_output_dir):
    """Example of using multiple fixtures."""
    # Use fixtures in your test
    assert sample_topic is not None
    assert mock_api_key.startswith("sk-ant-")
    assert temp_output_dir.exists()
```

### Mocking External Services

```python
def test_with_mocking(mocker):
    """Example of mocking external API calls."""
    # Mock Anthropic API
    mock_response = mocker.Mock()
    mocker.patch('anthropic.Anthropic.messages.create', return_value=mock_response)

    # Run test with mocked API
    # ...
```

### Testing File I/O

```python
def test_file_operations(temp_output_dir):
    """Example of testing file operations."""
    test_file = temp_output_dir / "test_output.md"
    test_file.write_text("Test content")

    assert test_file.exists()
    assert test_file.read_text() == "Test content"
```

## Coverage Goals

- **Target Coverage**: 70%+ overall
- **Critical Components**: 90%+ coverage
  - Content filtering logic
  - Crew coordination
  - Error handling paths

## Dependencies

Test dependencies are defined in `pyproject.toml` under `[project.optional-dependencies.test]`:

```toml
test = [
    "pytest>=8.0.0",        # Test framework
    "pytest-cov>=4.0.0",    # Coverage reporting
    "pytest-mock>=3.12.0",  # Mocking utilities
]
```

## Configuration

Pytest configuration is in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]           # Test directory
python_files = "test_*.py"      # Test file pattern
python_functions = "test_*"     # Test function pattern
addopts = "-v --tb=short"       # Default arguments
```

## Next Steps

1. **Install test dependencies**:

   ```bash
   uv sync --extra test
   ```

2. **Implement test cases** in placeholder files:
   - Start with `test_content_filter.py` for content safety
   - Add `test_crew.py` for core dialogue logic
   - Implement `test_gradio_app.py` for UI validation

3. **Run tests regularly** during development:

   ```bash
   make test-cov
   ```

4. **Maintain coverage** by adding tests for new features

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)
- [CrewAI Testing Guide](https://docs.crewai.com/)
