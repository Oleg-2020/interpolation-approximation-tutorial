# Contributing to MathDoc

Thank you for your interest in contributing to MathDoc! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/interpolation-approximation-tutorial.git
   cd interpolation-approximation-tutorial
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e .[dev]
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### Code Style

We follow PEP 8 style guidelines. Format your code using:

```bash
black .
isort .
```

### Linting

Check code quality:

```bash
flake8 mathdoc tests
mypy mathdoc
pylint mathdoc
```

### Testing

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=mathdoc --cov-report=html
```

### Documentation

Build documentation locally:

```bash
cd docs
make html
```

Documentation will be in `docs/build/html/`.

## Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request on GitHub

## Pull Request Guidelines

- Include a clear description of the changes
- Reference any related issues (e.g., "Closes #123")
- Ensure all tests pass
- Update documentation as needed
- Add tests for new functionality
- Follow the existing code style

## Commit Message Guidelines

Use clear, descriptive commit messages:

- Good: "Add Hermite basis function support"
- Good: "Fix numerical stability in Chebyshev approximation"
- Avoid: "Fix bug", "Update code"

## Adding Tests

Place tests in the `tests/` directory with names matching `test_*.py`. Use pytest fixtures and follow existing patterns:

```python
import pytest
from mathdoc import YourClass

def test_feature():
    """Test description."""
    obj = YourClass()
    result = obj.method()
    assert result == expected
```

## Adding Documentation

Update relevant `.rst` files in `docs/source/`. Use:

- `:class:`~mathdoc.ClassName`` for class references
- `:func:`~mathdoc.function_name`` for function references
- `:mod:`mathdoc.module_name`` for module references
- Mathematical equations in LaTeX format

## Reporting Issues

When reporting issues, please include:

- Python version
- Relevant dependencies and versions
- Minimal code example to reproduce
- Expected vs. actual behavior
- Relevant error messages and tracebacks

## Code of Conduct

Please be respectful and constructive in all interactions.

## Questions?

Feel free to open an issue for questions or discussions.

Thank you for contributing!
