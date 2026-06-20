# Changelog

All notable changes to Scrappy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Health check endpoint with Redis connectivity monitoring
- Single and bulk scraping endpoints
- Job status polling mechanism
- Webhook callback support for result delivery
- Intelligent engine selection (httpx vs Playwright)
- Automatic retry logic with exponential backoff
- robots.txt compliance checking
- Docker Compose setup for local development
- Comprehensive documentation and examples
- Security policy and guidelines

### Changed
- Initial release (version 0.1.0)

### Fixed
- Initial release

### Security
- Initial security release - see SECURITY.md

---

## [0.1.0] - 2026-06-20

### Added
- **Core API**: RESTful API for scraping operations
  - `GET /api/v1/health` - Service health monitoring
  - `POST /api/v1/scrape` - Single URL scraping
  - `POST /api/v1/scrape/bulk` - Batch scraping (up to 20 URLs)
  - `GET /api/v1/scrape/{job_id}` - Job status and result retrieval

- **Scraping Engines**:
  - httpx engine for fast, lightweight HTTP requests
  - Playwright engine for JavaScript-heavy and protected sites
  - Automatic engine selection based on domain analysis

- **Job Management**:
  - Asynchronous job queuing via Redis + arq
  - Job status tracking (queued, processing, complete, failed)
  - Configurable worker concurrency
  - Automatic retry with exponential backoff

- **Compliance & Safety**:
  - robots.txt validation and compliance
  - Request timeout enforcement
  - Domain-based engine selection for protected sites
  - Comprehensive error handling and recovery

- **Configuration**:
  - Pydantic-based settings management
  - Environment variable support
  - Redis connection pooling
  - Configurable concurrency and timeouts

- **Documentation**:
  - README with full API documentation
  - Getting Started guide with multiple deployment options
  - Contributing guidelines
  - Security policy
  - Code examples in Python and cURL
  - Interactive HTML demo
  - Postman API collection

- **Deployment**:
  - Docker and Docker Compose support
  - GitHub Actions CI/CD pipeline
  - Systemd service files
  - Shell scripts for easy startup
  - Production deployment guidelines

- **Examples**:
  - Python client example with full usage patterns
  - Webhook receiver example
  - Bulk and single scraping examples
  - Job polling and status checking examples

### Technical Details

- **Framework**: FastAPI 0.111+
- **Server**: Uvicorn 0.29+
- **Job Queue**: arq 0.25+
- **HTTP Client**: httpx 0.27+
- **Browser Automation**: Playwright 1.44+
- **Configuration**: Pydantic Settings 2.3+
- **HTML Parsing**: BeautifulSoup4 4.12+ and lxml 5.2+
- **Python**: 3.11+

### Known Limitations

- No built-in authentication (implement at reverse proxy)
- No request signing mechanism
- Results stored in Redis (configure persistence)
- Single Redis instance (no clustering in this version)
- No built-in rate limiting per client

### Performance Baseline

| Metric | Value |
|--------|-------|
| httpx Request | 100-200ms |
| Playwright Request | 2-5 seconds |
| Base Memory | ~50MB |
| httpx Job Memory | ~5MB |
| Playwright Job Memory | ~30MB |
| Default Concurrency | 10 |

---

## Version Numbering

This project uses Semantic Versioning:
- **MAJOR**: Breaking changes (0.x during alpha/beta)
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes and improvements

### Alpha/Beta Convention (0.x)
- 0.1.x - Experimental, API may change
- 0.2.x - Early adoption, core features stable
- 0.3.x - Release candidate preparation
- 1.0.0 - First stable release

---

## Planned Features

### High Priority (v0.2)
- [ ] Proxy rotation support
- [ ] Screenshot capture functionality
- [ ] Advanced caching strategies
- [ ] Per-domain rate limiting
- [ ] User authentication & API keys

### Medium Priority (v0.3)
- [ ] Distributed tracing (OpenTelemetry)
- [ ] Metrics export (Prometheus)
- [ ] Request/response logging
- [ ] Session management
- [ ] Cookie persistence

### Nice to Have (v1.0+)
- [ ] Graphical dashboard
- [ ] Analytics and reporting
- [ ] Custom header injection
- [ ] JavaScript execution callbacks
- [ ] Database result storage
- [ ] GraphQL query builder

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

## Support

- 📖 [Documentation](./README.md)
- 🚀 [Getting Started](./GETTING_STARTED.md)
- 🐛 [Issue Tracker](https://github.com/sam/scrappy/issues)
- 💬 [Discussions](https://github.com/sam/scrappy/discussions)

## License

MIT © 2026 Sam. See [LICENSE](./LICENSE) for details.

---

**Last Updated**: 2026-06-20
