# Changelog

All notable changes to AgentDNA will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Database encryption (SQLCipher integration)
- Desktop packaging (Tauri shell)
- API authentication (bearer tokens)
- Integration test suite
- CSRF protection
- Metrics and observability

## [0.1.0-alpha] - 2024-01-30

### Added
- Initial prototype release
- Core privacy-first architecture
- Agent lifecycle (NURSERY → ACTIVE → DORMANT → DEAD)
- Pattern detection and nursery shadow testing
- Fitness-based evolution engine
- FastAPI backend with 20+ endpoints
- Dashboard UI with real-time updates
- Privacy controls and allowlisting
- Comprehensive logging framework with JSON formatting
- Centralized error handling
- Token bucket rate limiting
- Environment configuration validation
- Redaction for sensitive data (emails, cards, API keys)
- Vector search for retrieval
- ReAct planning with policy gating
- SQLite persistence layer
- 19 unit tests covering core functionality
- GitHub Actions CI workflow
- Issue and PR templates

### Security
- Monitoring disabled by default
- Explicit app allowlisting required
- Sensitive app blocking (password managers, banking)
- API keys never exposed in status endpoints
- Loopback-only API binding
- No keystroke or clipboard content capture

### Fixed
- Missing `redact` import in activity_monitor.py (crash bug)
- Dev CORS origin removed from production config
- Dependencies pinned to exact versions

### Known Issues
- Database not encrypted (plain SQLite)
- No desktop packaging (CLI only)
- No API authentication
- No integration tests
- Manual testing required for platform adapters (Windows/Mac/Linux)

[Unreleased]: https://github.com/amg555/Agentdna/compare/v0.1.0-alpha...HEAD
[0.1.0-alpha]: https://github.com/amg555/Agentdna/releases/tag/v0.1.0-alpha
