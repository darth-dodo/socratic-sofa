# Changelog

All notable changes to Socratic Sofa will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2025-12-20

### Added

- **Security Scanning**: Bandit integration for vulnerability detection in CI pipeline
- **Secrets Detection**: detect-secrets with baseline for credential scanning
- **Enhanced CI/CD**: Split into 3 parallel jobs (quality, security, tests)

### Improved

- **Test Coverage**: Increased from 80% to 99% with 220+ tests
- **Documentation**: Updated testing guide with current test suite details
- **Architecture Docs**: Added mermaid diagrams for visual documentation
- **Pre-commit Hooks**: Full suite including isort, ruff, bandit, detect-secrets, vulture, prettier

### Fixed

- **CrewAI Tests**: Added mock OpenAI API key fixture for test isolation
- **Linting Issues**: Resolved unused imports and variable assignments

## [0.2.0] - 2024-12-19

### Added

- **Differentiation Scoring System**: Second inquiry now receives bonus points (0-10%) for exploring genuinely different philosophical angles
- **Repetition Penalty**: Judge agent penalizes overlapping questions or themes (up to -15%) to encourage intellectual diversity
- **Philosophical Traditions Integration**: Agents now draw from Greek, Eastern, Modern Western, and Contemporary philosophy
- **Markdown-Formatted Evaluation**: Judge output now uses formatted tables and emoji indicators for better readability
- **Category Organization**: 100 topics now organized into 7 categories (classics, ethics, mind, society, modern, fun, personal)
- **Streaming Output**: Real-time task completion feedback in Gradio UI
- **GitHub Actions CI/CD**: Automated testing and deployment pipeline
- **Comprehensive Test Suite**: 80%+ code coverage with pytest
- **Content Moderation**: AI-powered filtering for appropriate philosophical discourse
- **UV Package Manager**: Fast dependency management and virtual environment handling

### Changed

- **Judge Evaluation Criteria**: Enhanced scoring with explicit differentiation assessment
- **Task Instructions**: Updated `oppose` task to explicitly require different philosophical angles
- **Agent Backstories**: Enriched with multiple philosophical traditions
- **Current Year Context**: Tasks now include {current_year} parameter for relevant inquiries
- **Gradio UI**: Improved mobile responsiveness and progressive disclosure

### Technical

- **Framework**: CrewAI 1.7.0
- **LLM**: Upgraded to Claude Sonnet 4.5 for main dialogues
- **Testing**: pytest with coverage reporting
- **CI/CD**: GitHub Actions workflows for testing and deployment
- **Deployment**: HuggingFace Spaces with automated synchronization
- **Package Management**: Migrated to UV for faster installation

## [0.1.0] - 2024-12-15

### Added

- Initial release of Socratic Sofa
- Socratic Philosopher agent using authentic Socratic method
- Dialectic Moderator agent for evaluation
- 100 curated philosophical topics
- Four-stage dialogue system (Topic → Proposition → Opposition → Judgment)
- Mobile-responsive Gradio web interface
- Content moderation system
- CLI interface for command-line usage
- Comprehensive documentation

### Technical

- **Framework**: CrewAI for multi-agent orchestration
- **LLM**: Claude via Anthropic API
- **Interface**: Gradio 6.1.0
- **Process**: Sequential task execution
- **Output**: Markdown files for each dialogue stage

---

## Version Numbering

- **Major version (X.0.0)**: Incompatible API changes or major feature overhauls
- **Minor version (0.X.0)**: New features in a backwards-compatible manner
- **Patch version (0.0.X)**: Backwards-compatible bug fixes

## Upgrade Guide

### From 0.1.0 to 0.2.0

No breaking changes. Simply update dependencies:

```bash
# Update dependencies
uv sync

# Verify installation
uv run pytest
```

The new differentiation scoring and philosophical traditions features are automatically active.

## Future Plans

See [TASKS.md](../TASKS.md) for planned features and improvements.

## Links

- [GitHub Repository](https://github.com/darth-dodo/socratic-sofa)
- [HuggingFace Spaces](https://huggingface.co/spaces/darth-dodo/socratic-sofa)
- [Documentation](./README.md)
