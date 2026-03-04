# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-03-04

### Added
- Initial release of Kimi Device Authentication Bridge
- `KimiAuthBridge` class for synchronous token retrieval
- `AsyncKimiAuthBridge` class for async operations
- `KimiConfig` dataclass for configuration
- Comprehensive exception hierarchy
- Flask integration example
- FastAPI integration example
- Basic usage example
- Full test suite with pytest
- GitHub Actions CI/CD pipeline
- MIT License

### Features
- OAuth token retrieval from Kimi CLI credentials
- Secure token handling (read-only)
- User-Agent header management
- Authentication status checking
- Token preview for UI display
- Decorator for protected functions
- Login/logout command execution

### Security
- No hardcoded API keys
- No token caching in memory
- Read-only access to credentials
- Secure file permission handling

## [Unreleased]

### Planned
- Token refresh scheduling
- Multiple credential profiles
- Webhook support for token events
- Token usage analytics
- Caching layer with TTL
