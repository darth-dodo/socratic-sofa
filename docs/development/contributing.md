# Contributing Guidelines

Welcome to Socratic Sofa! This guide will help you contribute effectively to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Commit Conventions](#commit-conventions)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)
- [Review Process](#review-process)

## Code of Conduct

### Our Philosophy

Socratic Sofa embodies the Socratic method's principles:

- **Intellectual Humility**: Approach discussions professing what we don't know
- **Constructive Inquiry**: Challenge ideas through questions, not assertions
- **Respect**: Treat all contributors with dignity and respect
- **Open-mindedness**: Be willing to change your position based on evidence

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Trolling, insulting comments, or personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could be considered inappropriate in a professional setting

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. Completed the [Development Setup](setup.md)
2. Read the project [README](../../README.md)
3. Reviewed the [Architecture Documentation](../architecture.md)
4. Familiarized yourself with CrewAI concepts

### Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/socratic-sofa.git
cd socratic-sofa/socratic_sofa

# Add upstream remote
git remote add upstream https://github.com/darth-dodo/socratic-sofa.git

# Verify remotes
git remote -v
```

### Create a Feature Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name

# Examples:
# git checkout -b feature/add-new-agent
# git checkout -b fix/gradio-mobile-layout
# git checkout -b docs/improve-setup-guide
```

## Development Workflow

### 1. Make Changes

Edit files in your feature branch following the [Code Standards](#code-standards).

### 2. Test Locally

```bash
# Run linting
make lint

# Format code
make format

# Test CLI mode
make dev

# Test web interface
make web

# Run tests (when available)
make test
```

### 3. Commit Changes

Follow [Commit Conventions](#commit-conventions) for all commits.

```bash
# Stage changes
git add src/socratic_sofa/new_feature.py

# Commit with descriptive message
git commit -m "feat: add new Socratic questioning pattern"

# Or use interactive commit
git commit
```

### 4. Push to Your Fork

```bash
# Push feature branch
git push origin feature/your-feature-name
```

### 5. Create Pull Request

Open a pull request on GitHub following the [Pull Request Process](#pull-request-process).

## Code Standards

### Python Style Guide

We follow **PEP 8** with Ruff enforcement.

#### Formatting Rules

```python
# Use 4 spaces for indentation (no tabs)
def example_function():
    return "formatted code"

# Maximum line length: 88 characters (Black compatible)
long_variable_name = "Keep lines reasonably short for readability"

# Use double quotes for strings
message = "Hello, Socrates!"

# Two blank lines between top-level definitions
class MyClass:
    pass


def my_function():
    pass
```

#### Naming Conventions

```python
# Module names: lowercase with underscores
# my_module.py

# Class names: PascalCase
class SocraticDialogue:
    pass

# Function/variable names: snake_case
def generate_questions():
    question_count = 7
    return question_count

# Constants: UPPER_CASE
MAX_QUESTIONS = 10
API_TIMEOUT = 30

# Private methods: leading underscore
def _internal_helper():
    pass
```

#### Type Hints

Use type hints for function signatures:

```python
from typing import List, Dict, Optional, Tuple

def create_dialogue(
    topic: str,
    max_questions: int = 7,
    agent_config: Optional[Dict] = None
) -> List[str]:
    """
    Create a Socratic dialogue.

    Args:
        topic: The philosophical topic to explore
        max_questions: Maximum number of questions to generate
        agent_config: Optional agent configuration override

    Returns:
        List of generated Socratic questions
    """
    questions: List[str] = []
    return questions
```

#### Docstrings

Use Google-style docstrings:

```python
def evaluate_dialogue(
    proposition: str,
    opposition: str
) -> Tuple[int, str]:
    """
    Evaluate the quality of Socratic dialogues.

    This function assesses both dialogues using the dialectic moderator's
    criteria: question quality, elenctic effectiveness, philosophical
    insight, and Socratic fidelity.

    Args:
        proposition: The first line of Socratic inquiry
        opposition: The alternative line of inquiry

    Returns:
        A tuple of (score, evaluation_text) where score is 0-100

    Raises:
        ValueError: If either dialogue is empty or invalid

    Example:
        >>> score, evaluation = evaluate_dialogue(prop, opp)
        >>> print(f"Score: {score}/100")
        Score: 85/100
    """
    pass
```

### Code Organization

#### File Structure

```python
# Standard import order (Ruff enforces this)
# 1. Standard library imports
import os
import sys
from datetime import datetime
from typing import Dict, List

# 2. Third-party imports
import gradio as gr
from crewai import Agent, Task

# 3. Local imports
from socratic_sofa.crew import SocraticSofa
from socratic_sofa.content_filter import is_topic_appropriate
```

#### Function Length

- Keep functions under 50 lines when possible
- Extract complex logic into helper functions
- Use descriptive function names that explain intent

```python
# Good: Small, focused functions
def validate_topic(topic: str) -> bool:
    """Check if topic is valid for philosophical inquiry."""
    return bool(topic and len(topic.strip()) > 0)

def filter_inappropriate_content(topic: str) -> Tuple[bool, str]:
    """Apply AI moderation to topic."""
    return is_topic_appropriate(topic)

# Avoid: Large monolithic functions
def process_everything(topic: str):
    # 200 lines of mixed logic...
    pass
```

### Configuration Management

#### YAML Configuration

```yaml
# agents.yaml - Clear, documented structure
agent_name:
  role: >
    Brief, clear role description
  goal: >
    Specific, measurable goal
  backstory: >
    Context and methodology in 2-3 paragraphs.

    Use proper formatting and bullet points for clarity:
    - First principle
    - Second principle
    - Third principle
```

#### Environment Variables

```python
# Use environment variables for configuration
import os

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
SERVER_PORT = int(os.environ.get("PORT", "7860"))
DEBUG_MODE = os.environ.get("DEBUG", "false").lower() == "true"

# Provide defaults and validation
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable required")
```

### Error Handling

```python
# Use specific exceptions
def load_configuration(file_path: str) -> Dict:
    """Load configuration from YAML file."""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML configuration: {e}")

# Provide helpful error messages
def run_dialogue(topic: str) -> str:
    """Run Socratic dialogue on topic."""
    if not topic:
        raise ValueError(
            "Topic cannot be empty. Provide a philosophical question "
            "or use empty string to let AI choose."
        )
    # ... rest of implementation
```

## Commit Conventions

We follow **Conventional Commits** specification for clear, semantic commit messages.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

- **feat**: New feature for users
- **fix**: Bug fix for users
- **docs**: Documentation changes
- **style**: Formatting, missing semicolons, etc (no code change)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding or updating tests
- **chore**: Updating build tasks, package manager configs, etc

### Examples

```bash
# Feature addition
git commit -m "feat(agents): add epistemic humility to Socratic questioner

Enhance the Socratic agent with epistemic humility principle,
causing it to profess ignorance more explicitly before questioning.

Closes #42"

# Bug fix
git commit -m "fix(gradio): resolve mobile layout overflow issue

Mobile screens were experiencing horizontal scroll due to
fixed-width containers. Updated CSS to use responsive units.

Fixes #38"

# Documentation
git commit -m "docs(setup): add troubleshooting section for UV installation

Added common UV installation issues and their solutions based on
community feedback in issues #25 and #31."

# Breaking change
git commit -m "refactor(crew)!: change task output file naming scheme

BREAKING CHANGE: Output files renamed from descriptive names to
numbered scheme (01_topic.md, 02_proposition.md, etc.)

This improves sorting and programmatic access but existing scripts
that reference old names will need updates.

Refs #55"
```

### Commit Best Practices

1. **Use imperative mood**: "add feature" not "added feature"
2. **Capitalize first letter**: "Add feature" not "add feature"
3. **No period at the end**: "Add feature" not "Add feature."
4. **Keep subject under 50 characters**
5. **Wrap body at 72 characters**
6. **Separate subject from body with blank line**
7. **Use body to explain what and why, not how**
8. **Reference issues and PRs in footer**

## Pull Request Process

### Before Creating PR

1. **Update from upstream**:
   ```bash
   git checkout main
   git pull upstream main
   git checkout feature/your-feature
   git rebase main
   ```

2. **Ensure code quality**:
   ```bash
   make lint
   make format
   make test  # when available
   ```

3. **Test both interfaces**:
   ```bash
   make dev   # CLI mode
   make web   # Web interface
   ```

### PR Title and Description

#### Title Format

Follow commit convention format:

```
feat(agents): add new Socratic questioning pattern
fix(gradio): resolve mobile responsiveness issues
docs(contributing): clarify commit message guidelines
```

#### Description Template

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Changes Made
- Detailed list of changes
- File-by-file if significant
- Architecture/design decisions

## Testing
- [ ] CLI mode tested
- [ ] Web interface tested
- [ ] Unit tests added/updated (when applicable)
- [ ] Manual testing performed

## Screenshots (if applicable)
Include screenshots for UI changes.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Dependent changes merged

## Related Issues
Closes #XX
Refs #YY
```

### PR Size Guidelines

- **Small PRs preferred**: <300 lines changed
- **Break large changes** into multiple PRs when possible
- **One concern per PR**: Don't mix refactoring with features

### Draft PRs

Use draft PRs for work-in-progress:

```bash
# GitHub CLI
gh pr create --draft --title "WIP: feat(agents): new evaluation criteria"

# Or mark as draft in GitHub UI
```

## Testing Requirements

### Current State

The project is currently in early development. Tests will be added following this structure:

```
tests/
├── unit/
│   ├── test_crew.py
│   ├── test_content_filter.py
│   └── test_agents.py
├── integration/
│   ├── test_dialogue_flow.py
│   └── test_gradio_interface.py
└── fixtures/
    ├── sample_topics.py
    └── mock_responses.py
```

### Testing Standards (Future)

When adding tests:

```python
# Use pytest
import pytest
from socratic_sofa.crew import SocraticSofa

def test_topic_validation():
    """Test that topic validation rejects empty strings."""
    crew = SocraticSofa()
    with pytest.raises(ValueError, match="Topic cannot be empty"):
        crew.validate_topic("")

def test_question_generation():
    """Test that Socratic agent generates expected number of questions."""
    result = generate_socratic_questions("What is justice?", count=7)
    assert len(result) == 7
    assert all(q.strip().endswith("?") for q in result)

# Use fixtures for common test data
@pytest.fixture
def sample_topic():
    return "What is the nature of consciousness?"

def test_dialogue_with_fixture(sample_topic):
    """Test dialogue generation with sample topic."""
    result = run_dialogue(sample_topic)
    assert result is not None
```

### Manual Testing Checklist

For all PRs, manually verify:

- [ ] CLI mode runs without errors: `make dev`
- [ ] Web interface loads: `make web`
- [ ] Topic selection works (dropdown and custom input)
- [ ] All four dialogue stages generate correctly
- [ ] Mobile responsiveness (test on phone or browser dev tools)
- [ ] Content moderation catches inappropriate topics
- [ ] Error messages are user-friendly
- [ ] Output files created in `outputs/` directory

## Documentation

### When to Update Documentation

Update docs when you:

- Add new features or commands
- Change existing behavior
- Fix bugs that affect user experience
- Add configuration options
- Modify deployment process

### Documentation Standards

```markdown
# Use clear headings hierarchy

## Main Section

### Subsection

Brief introduction paragraph.

#### Code Examples

Always include working code examples:

\`\`\`python
# Example with comments
from socratic_sofa.crew import SocraticSofa

# Create crew instance
crew = SocraticSofa()
result = crew.run_dialogue("What is truth?")
\`\`\`

#### Command Examples

Show expected output:

\`\`\`bash
$ make dev
🏛️ Running Socratic dialogue (CLI)...
# ... output ...
✅ Dialogue complete!
\`\`\`
```

### Documentation Files to Update

- `README.md`: User-facing features and quick start
- `docs/architecture.md`: System design and agent configuration
- `docs/development/setup.md`: Environment setup changes
- `docs/development/contributing.md`: Process changes
- `docs/deployment.md`: Deployment configuration changes
- Inline code comments: Complex logic explanation

## Review Process

### What Reviewers Look For

1. **Code Quality**:
   - Follows style guidelines
   - Properly formatted (passes `make lint`)
   - Clear variable/function names
   - Appropriate comments

2. **Functionality**:
   - Solves stated problem
   - No unintended side effects
   - Edge cases handled
   - Error handling present

3. **Testing**:
   - Manual testing completed
   - Tests added/updated (when applicable)
   - No regressions introduced

4. **Documentation**:
   - Code comments for complex logic
   - Docstrings for public functions
   - README/docs updated if needed

5. **Architecture**:
   - Fits existing patterns
   - Doesn't add unnecessary complexity
   - Follows CrewAI best practices

### Addressing Review Comments

```bash
# Make requested changes
git add changed_files.py
git commit -m "fix: address review feedback on error handling"

# Push updates
git push origin feature/your-feature

# PR automatically updates
```

### Review Etiquette

**As a contributor**:
- Respond to all comments
- Ask for clarification if needed
- Don't take feedback personally
- Update PR based on feedback
- Mark conversations as resolved

**As a reviewer**:
- Be constructive and specific
- Praise good solutions
- Explain the "why" behind suggestions
- Offer alternatives, not just criticism
- Approve when satisfied

## Getting Help

### Resources

- **CrewAI Documentation**: https://docs.crewai.com
- **Gradio Guides**: https://gradio.app/guides
- **Anthropic API Docs**: https://docs.anthropic.com
- **Python Style Guide**: https://peps.python.org/pep-0008/

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Request Comments**: Code-specific discussions

### Common Questions

**Q: Can I work on an existing issue?**
A: Yes! Comment on the issue to let others know you're working on it.

**Q: How long before my PR is reviewed?**
A: We aim for initial review within 3-5 days. Complex PRs may take longer.

**Q: Can I contribute documentation only?**
A: Absolutely! Documentation improvements are highly valued.

**Q: What if my PR conflicts with main?**
A: Rebase your branch: `git rebase upstream/main` and resolve conflicts.

**Q: Should I create an issue first?**
A: For bugs and features, yes. For docs/typos, a direct PR is fine.

## Recognition

Contributors are recognized in:
- Git commit history
- GitHub contributors graph
- Release notes for significant contributions
- Project README (for major features)

Thank you for contributing to Socratic Sofa! Your efforts help bring philosophical inquiry to the AI age.

---

**Questions?** Open a discussion on GitHub or comment on relevant issues.
