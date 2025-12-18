# Testing Guide

Comprehensive testing guide for Socratic Sofa development.

## Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Current Testing State](#current-testing-state)
- [Manual Testing](#manual-testing)
- [Future Test Structure](#future-test-structure)
- [Test Development](#test-development)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Best Practices](#best-practices)

## Testing Philosophy

### Core Principles

Socratic Sofa testing follows these principles:

1. **Quality Over Quantity**: Meaningful tests that catch real issues
2. **Fast Feedback**: Quick-running tests for rapid development
3. **Comprehensive Coverage**: Test all critical paths
4. **Real-world Scenarios**: Tests reflect actual usage patterns
5. **Maintainable Tests**: Easy to understand and update

### Testing Pyramid

```
        /\
       /  \
      / E2E \      End-to-End (5-10%)
     /______\
    /        \
   /Integration\   Integration (20-30%)
  /____________\
 /              \
/  Unit Tests    \  Unit (60-75%)
/_________________\
```

## Current Testing State

### Status

The project is currently in **early development phase** without formal test suite. Testing is performed manually using:

- CLI mode execution (`make dev`)
- Web interface testing (`make web`)
- Code quality checks (`make lint`)
- Manual verification of outputs

### Why No Tests Yet?

- **Rapid prototyping phase**: Core functionality still evolving
- **Agent behavior validation**: CrewAI agent interactions require special testing approaches
- **AI output variability**: Testing non-deterministic AI responses requires specialized frameworks

### When Will Tests Be Added?

Tests will be added when:

1. Core architecture stabilizes
2. Agent configurations finalize
3. API contracts solidify
4. Common failure patterns emerge

## Manual Testing

Until automated tests are implemented, follow these manual testing procedures.

### Pre-Commit Testing Checklist

Before committing code, verify:

```bash
# 1. Code quality passes
make lint

# 2. Code is properly formatted
make format

# 3. CLI mode works
make dev

# 4. Web interface launches
make web
```

### CLI Mode Testing

#### Basic Functionality Test

```bash
# Run with default topic
make dev

# Expected behavior:
# ✅ Crew initializes without errors
# ✅ Four tasks execute sequentially:
#    - propose_topic
#    - propose
#    - oppose
#    - judge_task
# ✅ Four output files created in outputs/
# ✅ Completion time: 2-3 minutes
# ✅ No Python errors or warnings

# Verify outputs
ls -lh outputs/
cat outputs/01_topic.md
cat outputs/02_proposition.md
cat outputs/03_opposition.md
cat outputs/04_judgment.md
```

#### Custom Topic Test

```bash
# Test with custom topic in main.py
# Edit src/socratic_sofa/main.py:
# inputs = {'topic': 'What is consciousness?', ...}

uv run socratic_sofa

# Verify:
# ✅ Topic is used in dialogue
# ✅ Questions relate to consciousness
# ✅ No generic fallback topics
```

#### Error Handling Test

```bash
# Test with invalid API key
export ANTHROPIC_API_KEY="invalid_key"
make dev

# Expected:
# ❌ Clear error message about API key
# ❌ No stack trace exposed to user

# Restore valid key
export ANTHROPIC_API_KEY="your_valid_key"
```

### Web Interface Testing

#### Desktop Browser Test

```bash
# Launch interface
make web

# Open http://localhost:7860
```

**Test cases**:

1. **Page Load**:
   - [ ] Interface loads without errors
   - [ ] All sections visible
   - [ ] Buttons are clickable
   - [ ] Dropdown populated with topics

2. **Topic Selection - Dropdown**:
   - [ ] Select "Let AI choose"
   - [ ] Click "Begin Socratic Dialogue"
   - [ ] AI proposes a topic
   - [ ] Select specific topic from dropdown
   - [ ] Topic is used in dialogue

3. **Topic Selection - Custom Input**:
   - [ ] Type custom topic: "Should we colonize Mars?"
   - [ ] Leave dropdown at default
   - [ ] Custom topic takes priority
   - [ ] Dialogue uses custom topic

4. **Dialogue Execution**:
   - [ ] Progress indicator shows during execution
   - [ ] All four sections populate:
     - Proposed Topic
     - First Line of Inquiry
     - Alternative Line of Inquiry
     - Dialectic Evaluation
   - [ ] Markdown renders correctly (headers, lists, emphasis)
   - [ ] Questions are numbered 1-7
   - [ ] No truncated output

5. **Content Moderation**:
   - [ ] Enter inappropriate topic
   - [ ] Moderation catches it
   - [ ] Alternative suggestions shown
   - [ ] Clear error message displayed

6. **Error Handling**:
   - [ ] Test with no API key (if possible)
   - [ ] Error messages user-friendly
   - [ ] No stack traces shown to users

#### Mobile Browser Test

Test on actual mobile device or browser dev tools (iPhone X, Galaxy S10 sizes):

```bash
# Launch interface
make web

# Access from mobile device on same network
# http://YOUR_COMPUTER_IP:7860
```

**Mobile-specific test cases**:

1. **Layout**:
   - [ ] No horizontal scroll
   - [ ] Columns stack vertically
   - [ ] Text readable without zooming
   - [ ] Buttons full-width and touch-friendly (48px+ height)

2. **Input**:
   - [ ] Dropdown usable with touch
   - [ ] Text input shows mobile keyboard
   - [ ] Button tap responsive (not double-tap required)

3. **Output**:
   - [ ] Markdown renders correctly
   - [ ] Code blocks (if any) scroll horizontally
   - [ ] Lists formatted properly
   - [ ] Headers sized appropriately

4. **Performance**:
   - [ ] Interface loads quickly (<3s on 4G)
   - [ ] No jank during scrolling
   - [ ] Dialogue execution shows progress

#### Browser Compatibility Test

Test on multiple browsers:

- [ ] **Chrome/Edge** (Chromium): Latest version
- [ ] **Firefox**: Latest version
- [ ] **Safari**: Latest version (macOS/iOS)

Common issues to check:

- CSS flexbox support
- JavaScript ES6 features
- WebSocket connections (for Gradio)
- Markdown rendering

### Integration Testing

#### End-to-End Flow Test

Test complete user journey:

```bash
# 1. Fresh start
make clean
make install
make setup-env
# Add API key to .env

# 2. Launch web interface
make web

# 3. Execute flow:
#    - Select topic from dropdown
#    - Click begin
#    - Wait for completion
#    - Verify all outputs
#    - Check outputs/ directory
#    - Verify files created

# 4. Try second dialogue:
#    - Enter custom topic
#    - Execute
#    - Verify output files overwritten
#    - Content is new, not cached
```

#### Configuration Testing

```bash
# Test with modified agent configuration
# Edit src/socratic_sofa/config/agents.yaml
# Add new principle to Socratic questioner

# Run dialogue
make dev

# Verify:
# ✅ Configuration loaded
# ✅ Agent behavior reflects changes
# ✅ No YAML parsing errors

# Revert changes
git checkout src/socratic_sofa/config/agents.yaml
```

### Performance Testing

#### Response Time Test

```bash
# Time CLI execution
time make dev

# Expected:
# real    2m30s  (2-3 minutes typical)
# user    0m15s
# sys     0m2s

# If slower than 5 minutes, investigate:
# - API rate limits
# - Network latency
# - System resources
```

#### Memory Usage Test

```bash
# Monitor memory during execution
# Terminal 1:
make web

# Terminal 2:
watch -n 1 'ps aux | grep gradio | grep -v grep'

# Expected:
# Memory usage: 200-500 MB
# Should remain stable during execution
# No memory leaks after multiple dialogues
```

#### Concurrent User Test

```bash
# Launch interface
make web

# Open multiple browser tabs
# Execute dialogues simultaneously in 3+ tabs

# Verify:
# ✅ All requests complete
# ✅ No mixed responses between tabs
# ✅ No crashes or errors
# ✅ Each tab gets independent results
```

## Future Test Structure

When automated tests are implemented, this will be the structure:

### Directory Layout

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Fast, isolated tests
│   ├── __init__.py
│   ├── test_crew.py         # CrewAI setup tests
│   ├── test_content_filter.py  # Content moderation
│   ├── test_config.py       # Configuration loading
│   └── test_utils.py        # Utility functions
├── integration/             # Component interaction tests
│   ├── __init__.py
│   ├── test_dialogue_flow.py   # End-to-end dialogue
│   ├── test_gradio_app.py     # Web interface
│   └── test_agent_interactions.py  # Agent collaboration
├── fixtures/                # Test data and mocks
│   ├── __init__.py
│   ├── sample_topics.py     # Topic test data
│   ├── mock_responses.py    # Mocked API responses
│   └── config_samples.py    # Test configurations
└── e2e/                     # Browser-based tests
    ├── __init__.py
    └── test_web_interface.py  # Playwright/Selenium tests
```

### Test Running Commands

```bash
# Run all tests
make test

# Run specific test file
uv run pytest tests/unit/test_crew.py -v

# Run with coverage
uv run pytest --cov=src/socratic_sofa --cov-report=html

# Run only unit tests
uv run pytest tests/unit/ -v

# Run only integration tests
uv run pytest tests/integration/ -v

# Run with markers
uv run pytest -m slow       # Only slow tests
uv run pytest -m "not slow" # Skip slow tests
```

## Test Development

### Unit Test Example

```python
# tests/unit/test_content_filter.py
import pytest
from socratic_sofa.content_filter import (
    is_topic_appropriate,
    get_alternative_suggestions
)

class TestContentFilter:
    """Test suite for content moderation functionality."""

    def test_empty_topic_is_allowed(self):
        """Empty topics should be allowed (AI will choose)."""
        is_appropriate, reason = is_topic_appropriate("")
        assert is_appropriate is True
        assert reason == ""

    def test_philosophical_topic_is_allowed(self):
        """Standard philosophical topics should pass moderation."""
        is_appropriate, reason = is_topic_appropriate("What is justice?")
        assert is_appropriate is True
        assert reason == ""

    def test_long_topic_is_rejected(self):
        """Topics over 500 characters should be rejected."""
        long_topic = "A" * 501
        is_appropriate, reason = is_topic_appropriate(long_topic)
        assert is_appropriate is False
        assert "too long" in reason.lower()

    def test_alternative_suggestions_returned(self):
        """Alternative suggestions should be non-empty list."""
        suggestions = get_alternative_suggestions()
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        assert all(isinstance(s, str) for s in suggestions)

    @pytest.mark.slow
    def test_inappropriate_content_rejected(self):
        """Inappropriate content should be caught by AI moderation."""
        # Note: This makes real API call, marked as slow
        is_appropriate, reason = is_topic_appropriate("explicit violence topic")
        assert is_appropriate is False
        assert len(reason) > 0
```

### Integration Test Example

```python
# tests/integration/test_dialogue_flow.py
import pytest
from pathlib import Path
from socratic_sofa.crew import SocraticSofa

class TestDialogueFlow:
    """Test complete dialogue execution flow."""

    @pytest.fixture
    def crew(self):
        """Create SocraticSofa crew instance."""
        return SocraticSofa()

    @pytest.fixture
    def sample_inputs(self):
        """Sample inputs for dialogue."""
        return {
            'topic': 'What is consciousness?',
            'current_year': '2024'
        }

    @pytest.fixture(autouse=True)
    def cleanup_outputs(self):
        """Clean output directory before and after tests."""
        output_dir = Path("outputs")
        for file in output_dir.glob("*.md"):
            file.unlink()
        yield
        for file in output_dir.glob("*.md"):
            file.unlink()

    def test_full_dialogue_execution(self, crew, sample_inputs):
        """Test complete dialogue from start to finish."""
        # Execute crew
        result = crew.crew().kickoff(inputs=sample_inputs)

        # Verify result exists
        assert result is not None
        assert hasattr(result, 'raw')

        # Verify output files created
        output_files = [
            "outputs/01_topic.md",
            "outputs/02_proposition.md",
            "outputs/03_opposition.md",
            "outputs/04_judgment.md"
        ]

        for file_path in output_files:
            assert Path(file_path).exists(), f"Missing output: {file_path}"
            content = Path(file_path).read_text()
            assert len(content) > 0, f"Empty output: {file_path}"

    def test_proposition_contains_questions(self, crew, sample_inputs):
        """Test that proposition output contains numbered questions."""
        crew.crew().kickoff(inputs=sample_inputs)

        content = Path("outputs/02_proposition.md").read_text()

        # Should contain numbered questions
        assert "1." in content
        assert "?" in content
        # Should have multiple questions
        question_count = content.count("?")
        assert question_count >= 5, f"Expected 5+ questions, found {question_count}"

    def test_judgment_contains_scores(self, crew, sample_inputs):
        """Test that judgment contains evaluation scores."""
        crew.crew().kickoff(inputs=sample_inputs)

        content = Path("outputs/04_judgment.md").read_text()

        # Should contain scoring keywords
        assert any(word in content.lower() for word in ["score", "percentage", "%"])
        assert any(word in content.lower() for word in ["quality", "effectiveness", "insight"])
```

### Fixture Example

```python
# tests/conftest.py
import pytest
import os
from pathlib import Path

@pytest.fixture(scope="session")
def test_api_key():
    """Provide test API key or skip if not available."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY not set")
    return api_key

@pytest.fixture
def mock_anthropic_response():
    """Mock Anthropic API response for testing."""
    return {
        "content": [
            {"text": "APPROPRIATE"}
        ]
    }

@pytest.fixture
def sample_topics():
    """Provide sample philosophical topics for testing."""
    return [
        "What is justice?",
        "What is the good life?",
        "Can virtue be taught?",
        "What is consciousness?",
        "Do we have free will?"
    ]

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create temporary output directory for tests."""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    return output_dir
```

## Test Coverage

### Coverage Goals

- **Overall**: 80%+ code coverage
- **Critical paths**: 100% coverage
  - Content moderation
  - Configuration loading
  - Agent initialization
  - Error handling

### Measuring Coverage

```bash
# Generate coverage report
uv run pytest --cov=src/socratic_sofa --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html

# Coverage by file
uv run pytest --cov=src/socratic_sofa --cov-report=term-missing

# Coverage for specific module
uv run pytest --cov=src/socratic_sofa.content_filter tests/unit/test_content_filter.py
```

### Coverage Configuration

```ini
# pyproject.toml or .coveragerc
[tool.coverage.run]
source = ["src/socratic_sofa"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/.venv/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

## Best Practices

### Test Writing Guidelines

1. **Arrange-Act-Assert Pattern**:

   ```python
   def test_example():
       # Arrange: Set up test data
       topic = "What is justice?"

       # Act: Execute the code being tested
       result = process_topic(topic)

       # Assert: Verify the results
       assert result is not None
       assert "justice" in result.lower()
   ```

2. **Descriptive Test Names**:

   ```python
   # Good
   def test_empty_topic_returns_ai_generated_question():
       pass

   # Avoid
   def test_topic():
       pass
   ```

3. **One Assertion Per Test** (when reasonable):

   ```python
   # Good
   def test_topic_validation_rejects_empty_string():
       assert not validate_topic("")

   def test_topic_validation_accepts_valid_question():
       assert validate_topic("What is truth?")

   # Avoid combining unrelated assertions
   def test_everything():
       assert condition1
       assert condition2
       assert condition3  # If this fails, we don't know about condition4
       assert condition4
   ```

4. **Use Fixtures for Common Setup**:

   ```python
   @pytest.fixture
   def configured_crew():
       crew = SocraticSofa()
       crew.configure(test_mode=True)
       return crew

   def test_with_fixture(configured_crew):
       result = configured_crew.run()
       assert result is not None
   ```

5. **Mark Slow Tests**:

   ```python
   import pytest

   @pytest.mark.slow
   def test_full_dialogue_execution():
       # Test that takes >10 seconds
       pass
   ```

6. **Mock External Dependencies**:

   ```python
   from unittest.mock import patch, MagicMock

   def test_content_filter_with_mock():
       with patch('socratic_sofa.content_filter.Anthropic') as mock_client:
           mock_client.return_value.messages.create.return_value = MagicMock(
               content=[{"text": "APPROPRIATE"}]
           )
           is_appropriate, _ = is_topic_appropriate("Test topic")
           assert is_appropriate is True
   ```

### Testing AI/LLM Components

Special considerations for testing CrewAI agents:

1. **Test Configuration, Not Responses**:

   ```python
   # Test that agent is configured correctly
   def test_socratic_agent_configuration():
       agent = crew.socratic_questioner()
       assert agent.role == "Socratic Philosopher"
       assert "question" in agent.goal.lower()
   ```

2. **Test Structure, Not Content**:

   ```python
   # Test output structure, not specific philosophical content
   def test_dialogue_has_required_questions():
       result = generate_questions(topic)
       assert len(result) >= 5
       assert all(q.strip().endswith("?") for q in result)
   ```

3. **Use Deterministic Tests for Deterministic Code**:

   ```python
   # Test parsing logic, not AI generation
   def test_question_parsing():
       raw_output = "1. Question one?\n2. Question two?"
       questions = parse_questions(raw_output)
       assert len(questions) == 2
   ```

4. **Mock API Calls in Unit Tests**:
   ```python
   # Don't make real API calls in unit tests
   @patch('anthropic.Anthropic')
   def test_moderation_logic(mock_client):
       mock_client.return_value.messages.create.return_value = mock_response
       # Test logic without real API call
   ```

### Continuous Integration Testing

When CI is set up, tests should run on:

- Push to any branch
- Pull request creation
- Scheduled daily runs

```yaml
# .github/workflows/test.yml (example)
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.12"
      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Install dependencies
        run: uv sync
      - name: Run linting
        run: uv run ruff check src/
      - name: Run tests
        run: uv run pytest tests/ -v --cov
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Next Steps

1. Start with manual testing using checklists above
2. Identify common failure patterns
3. Write unit tests for utility functions
4. Add integration tests for dialogue flow
5. Implement E2E tests for web interface
6. Set up CI/CD for automated testing

## Resources

- **Pytest Documentation**: https://docs.pytest.org/
- **CrewAI Testing**: https://docs.crewai.com/core-concepts/Testing-Crews
- **Gradio Testing**: https://gradio.app/guides/testing
- **Python Testing Best Practices**: https://realpython.com/pytest-python-testing/

---

**Note**: This testing guide will evolve as the project matures and automated tests are implemented. Contributions to the test suite are highly encouraged!
