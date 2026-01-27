# Memory Match Backend

This directory contains the backend services for the Memory Match arcade game.

## Documentation

The API is documented using the OpenAPI Specification. You can find the definition in:
- [openapi.yaml](openapi.yaml)

## Package Management

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management and virtual environments.

### Prerequisites

- Python 3.8+

### Installing uv

If you don't have `uv` installed, you can install it using one of the following methods:

**Using pip (Recommended for this environment):**
```sh
pip install uv
```

**Using the official installer (MacOS/Linux):**
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Using the official installer (Windows):**
```powershell
powershell -c "irel ast.sh/uv/install.ps1 | iex"
```

### Getting Started

Once `uv` is installed, you can use it to manage the project:

```sh
# Install dependencies (defined in pyproject.toml)
uv sync

# Run the application
uv run python -m app.main

# Run tests
uv run pytest tests/
```

## Testing Structure

The test suite is located in the `tests/` directory and is split by functionality:
- `tests/test_auth.py`: Authentication endpoints (signup, login).
- `tests/test_leaderboard.py`: Leaderboard endpoints (GET, POST).
- `tests/conftest.py`: Shared fixtures (HTTP client).
