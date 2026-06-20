# Contributing to Scrappy

Thank you for your interest in contributing to Scrappy! We welcome contributions of all kinds, including bug reports, feature requests, documentation improvements, and code contributions.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Redis server
- Git

### Local Development Setup

1. **Fork the repository** and clone it locally:
   ```bash
   git clone https://github.com/your-username/scrappy.git
   cd scrappy
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8 mypy
   ```

4. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

5. **Start Redis:**
   ```bash
   redis-server
   ```

## Development Workflow

### Code Style

We follow PEP 8 with some enhancements. Please format your code before committing:

```bash
# Format code with black
black .

# Check code style
flake8 .

# Type checking
mypy .
```

### Testing

Run tests before submitting a pull request:

```bash
pytest
pytest --cov=.  # With coverage report
```

### Commit Messages

Please write clear, descriptive commit messages:

```
✨ feature: Add smart caching for robots.txt

- Cache robots.txt responses for 24 hours
- Reduce unnecessary network requests
- Add cache invalidation logic
```

### Pull Request Process

1. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/add-feature-name
   ```

2. **Make your changes** and commit them:
   ```bash
   git add .
   git commit -m "✨ feature: description"
   ```

3. **Push to your fork:**
   ```bash
   git push origin feature/add-feature-name
   ```

4. **Open a Pull Request** with a clear description of your changes

### Commit Message Prefixes

- ✨ `feature:` - New feature
- 🐛 `fix:` - Bug fix
- 📝 `docs:` - Documentation changes
- 🎨 `style:` - Code style changes (formatting, etc.)
- ♻️ `refactor:` - Code refactoring
- ⚡ `perf:` - Performance improvements
- ✅ `test:` - Adding or updating tests
- 🔧 `chore:` - Build process, dependencies, etc.

## Areas for Contribution

### High Priority

- [ ] Additional scraping engine support (Selenium, Pyppeteer)
- [ ] Proxy rotation integration
- [ ] Advanced caching strategies
- [ ] Rate limiting per domain
- [ ] Screenshot capture support
- [ ] Better error recovery

### Documentation

- [ ] API documentation improvements
- [ ] Tutorial articles
- [ ] Architecture deep-dives
- [ ] Deployment guides for different platforms
- [ ] Example projects

### Testing

- [ ] Unit test expansion
- [ ] Integration tests
- [ ] Performance benchmarks
- [ ] Load testing scenarios

## Bug Reports

When reporting bugs, please include:

1. **Description** - What behavior did you observe?
2. **Expected** - What did you expect to happen?
3. **Steps to Reproduce** - How can we reproduce the issue?
4. **Environment**:
   - OS (Windows, macOS, Linux)
   - Python version
   - Relevant dependencies
5. **Logs** - Any error messages or logs

## Feature Requests

Feature requests are welcome! Please include:

1. **Description** - What would you like to add?
2. **Use Case** - Why do you need this feature?
3. **Example** - How would you use it?

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our Code of Conduct.

### Our Standards

Examples of behavior that contributes to creating a positive environment:

- Using welcoming and inclusive language
- Being respectful of differing opinions and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior:

- The use of sexualized language or imagery
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## Questions or Need Help?

- Check existing [GitHub Issues](https://github.com/sam/scrappy/issues)
- Review the [Documentation](./README.md)
- See [Getting Started Guide](./GETTING_STARTED.md)

## Recognition

Contributors will be recognized in:

- README.md file
- Release notes
- Project contributors list

Thank you for helping make Scrappy better! 🕷️
