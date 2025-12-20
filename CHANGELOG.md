# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Structured logging system (`logging_config.py`) with:
  - JSON-formatted log output option via environment variable `JSON_LOGS=true`
  - Context-aware logger adapters for operation tracking
  - Timing context managers (`log_time`) and decorators (`timed`) for performance monitoring
  - Hierarchical logging under `socratic_sofa.*` namespace for better organization
- Rate limiting for API calls (`rate_limiter.py`) using `ratelimit` library:
  - Automatic retry decorator `@rate_limited()` with configurable retry attempts
  - Non-retry decorator `@rate_limited_no_retry()` for immediate failure scenarios
  - Content moderation limited to 10 calls per 60 seconds to prevent API throttling
  - Configurable rate limits via environment variables
- Comprehensive edge case tests (`tests/test_edge_cases.py`) covering:
  - Empty input handling
  - Maximum length inputs
  - Unicode and special character processing
  - Malformed API responses
  - Network timeout scenarios
- New dependency: `ratelimit>=2.2.1` for API rate limiting

### Changed

- `content_filter.py` now uses structured logging instead of print statements for better observability
- `content_filter.py` now applies rate limiting to OpenAI API calls to prevent throttling
- `gradio_app.py` now uses structured logging for consistent logging behavior
- Test coverage increased to 99% with comprehensive rate limiter and edge case tests
- Improved error handling and resilience throughout the codebase

### Fixed

- Potential API rate limiting issues by implementing proper rate control
- Logging inconsistencies by standardizing on structured logging approach

## [0.1.0] - 2025-12-20

### Added

- Initial release of Socratic Sofa
- Interactive Socratic dialogue system powered by CrewAI
- Content filtering for inappropriate inputs
- Progress indicators during dialogue generation
- Dialogue export functionality
- Support for customizable inquiry depth (3, 5, or 7 questions)
- Themed alternative inquiry suggestions
- Comprehensive test suite with 99% coverage
- Docker support for containerized deployment
- Gradio-based web interface

### Security

- OpenAI API key validation and secure handling
- Content moderation for user inputs
