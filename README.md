# Scrappy API Core

> The core FastAPI web scraping service. This repository contains only the production-ready application code for Scrappy.

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.111%2B-009688)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## About

Scrappy API Core is the core application layer of Scrappy, a production-grade asynchronous web scraping service. This repository contains the clean, optimized application code without development tools, examples, or Docker configurations.


## Quick Overview

Scrappy intelligently routes scraping requests based on target domain characteristics:

- **Lightweight domains** → Rapid httpx HTTP requests (100-200ms)
- **Heavy domains** → Full Playwright browser automation (2-5s)
- **Asynchronous** → Built on FastAPI and arq for high concurrency
- **Resilient** → Automatic retries, error recovery, job queuing
- **Compliant** → Respects robots.txt, configurable timeouts

## File Structure

```
├── main.py              # FastAPI application & lifespan
├── config.py            # Configuration management (Pydantic)
├── models.py            # Request/response data models
├── routes.py            # API endpoints (/scrape, /health, etc.)
├── worker.py            # Job processing & scraping logic
├── dependencies.py      # Engine selection & dependency injection
├── requirements.txt     # Python dependencies
└── .gitignore          # Git ignore patterns
```

## Core Dependencies

```
fastapi>=0.111.0              # Modern async web framework
uvicorn[standard]>=0.29.0     # ASGI server
arq>=0.25.0                   # Job queue
httpx>=0.27.0                 # Lightweight HTTP client
playwright>=1.44.0            # Browser automation
pydantic-settings>=2.3.0      # Configuration
beautifulsoup4>=4.12.0        # HTML parsing
lxml>=5.2.0                   # XML/HTML processing
```

## API Endpoints

**All endpoints use `/api/v1` prefix**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Service health check |
| POST | `/scrape` | Queue single URL |
| POST | `/scrape/bulk` | Queue multiple URLs |
| GET | `/scrape/{job_id}` | Check job status |

See the [full documentation](https://github.com/sam/scrappy) for detailed API specs.

## Configuration

Set environment variables or create a `.env` file:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
WORKER_CONCURRENCY=10
REQUEST_TIMEOUT=30
```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Running

Requires Redis service running on port 6379.

```bash
# Start API server
uvicorn main:app --host 0.0.0.0 --port 8000

# In another terminal, start workers
arq main.worker_jobs
```

## Development

Code organization:

- **main.py** - Application factory and lifecycle
- **config.py** - Settings and environment management  
- **models.py** - Pydantic models for validation
- **routes.py** - HTTP endpoint handlers
- **worker.py** - Job execution and scraping logic
- **dependencies.py** - Engine selection and helpers

### Code Standards

- Python 3.11+
- Type hints throughout
- PEP 8 compliant
- Docstrings for all public functions

## Integration

Use as a library:

```python
from fastapi import FastAPI
from main import app as scrappy_app

# Use Scrappy's routers
my_app = FastAPI()
my_app.include_router(scrappy_app.routes[0])
```

Or deploy as a standalone service and call via HTTP.

## Deployment

This core package is designed to be deployed in:
- Docker containers
- Kubernetes pods
- Traditional servers (systemd)
- Serverless platforms

For production deployment, see the [main Scrappy documentation](https://github.com/sam/scrappy/blob/main/README.md#deployment).

## Performance Characteristics

| Metric | Value |
|--------|-------|
| httpx latency | 100-200ms |
| Playwright latency | 2-5 seconds |
| Base memory | ~50MB |
| Per-job memory (httpx) | ~5MB |
| Per-job memory (Playwright) | ~30MB |
| Max concurrent (default) | 10 |

## License

Ahoy © 2026 Sam
