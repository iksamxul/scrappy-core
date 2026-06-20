# Security Policy

## Reporting Security Issues

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability, please email us at security@example.com with:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

We will acknowledge receipt within 48 hours and provide a timeline for resolution.

## Supported Versions

| Version | Supported | Notes |
|---------|-----------|-------|
| 0.1.x | ✅ Current | Latest development version |
| < 0.1.0 | ❌ Not released | N/A |

## Security Practices

### Input Validation

- All URL inputs validated using Pydantic's `HttpUrl`
- Request bodies validated against schema
- Domain names validated before processing

### Access Control

- API endpoints have no built-in authentication (use reverse proxy)
- Redis connection password support (configure via `REDIS_PASSWORD`)
- Environment variables for sensitive configuration

### Data Protection

- Sensitive data not logged
- Results stored in Redis (configure persistent storage)
- Webhook delivery uses HTTPS (enforce in configuration)

### Dependency Management

- Regular dependency updates
- Security patch prioritization
- Automated vulnerability scanning via Trivy
- No known critical vulnerabilities

### Rate Limiting

- Per-domain rate limiting recommended for production
- Request timeouts enforced
- Concurrent job limits configurable

### Network Security

- HTTPS recommended for API endpoints
- Redis over TLS recommended for production
- Firewall rules for internal services

## Known Limitations

1. **No built-in authentication** - Implement at reverse proxy level (nginx, AWS ALB, etc.)
2. **No request signing** - Use network security and reverse proxy authentication
3. **No encrypted storage** - Use encrypted Redis and encrypted filesystem
4. **No audit logging** - Implement via application monitoring tools

## Best Practices for Deployment

### ✅ Do

- [ ] Use strong `REDIS_PASSWORD`
- [ ] Enable Redis persistence (AOF or RDB)
- [ ] Use HTTPS/TLS for all connections
- [ ] Implement authentication at reverse proxy
- [ ] Use environment-specific `.env` files
- [ ] Enable firewall rules
- [ ] Monitor logs and alerts
- [ ] Regular security patches
- [ ] Keep dependencies updated
- [ ] Use secrets management (vault, AWS Secrets, etc.)

### ❌ Don't

- [ ] Don't expose Redis directly to internet
- [ ] Don't hardcode secrets in code
- [ ] Don't disable timeout protections
- [ ] Don't ignore security warnings
- [ ] Don't use default credentials
- [ ] Don't skip input validation
- [ ] Don't log sensitive data
- [ ] Don't disable HTTPS in production

## Security Headers

Recommended headers for reverse proxy:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

## Dependency Vulnerabilities

To check for known vulnerabilities:

```bash
# Using pip-audit
pip install pip-audit
pip-audit

# Using safety
pip install safety
safety check
```

## Deployment Security

### Docker

```dockerfile
# Use specific Python version
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 scrappy

# Set working directory
WORKDIR /app

# Install dependencies as root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application as root
COPY --chown=scrappy:scrappy . .

# Switch to non-root user
USER scrappy

# Run with non-root user
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: scrappy-api
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
  containers:
  - name: api
    image: scrappy:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
    resources:
      requests:
        memory: "128Mi"
        cpu: "100m"
      limits:
        memory: "512Mi"
        cpu: "500m"
```

## Environment Variables

Keep sensitive data in environment variables, never hardcode:

```bash
# Use strong passwords
REDIS_PASSWORD=your-strong-password-here

# Use secure webhook URLs
WEBHOOK_SIGNING_SECRET=your-secret

# Use specific hosts
REDIS_HOST=redis.internal
```

## Monitoring & Logging

### Log Sensitive Information

```python
# ❌ Don't
logger.info(f"Scraping {url} with result {result}")

# ✅ Do
logger.info(f"Job {job_id} completed successfully")
```

### Monitor These Events

- Failed authentication attempts
- Unusual concurrency levels
- Memory/CPU spikes
- Redis connection issues
- Rate limit violations
- Webhook delivery failures

## Security Audit Checklist

- [ ] All dependencies are up to date
- [ ] No hardcoded credentials
- [ ] Input validation enabled
- [ ] Timeouts configured
- [ ] Rate limiting enabled
- [ ] Logging configured (without secrets)
- [ ] Firewall rules in place
- [ ] HTTPS/TLS enabled
- [ ] Database backups configured
- [ ] Monitoring and alerting configured

## Contact

For security-related questions or to report issues:
- Security Email: security@example.com
- Response Time: 48 hours

Thank you for helping keep Scrappy secure! 🕷️
