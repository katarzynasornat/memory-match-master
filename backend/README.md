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

Once `uv` is installed, you can use the provided `Makefile` for convenience:

```sh
make install    # Install dependencies
make dev        # Start development server (hot-reload)
make run        # Start production server
make test       # Run tests
make lint       # Run lint checks
make format     # Format code
```

### Manual Commands
If you prefer running commands manually:
### Running the Server

1. **Install dependencies**:
   ```sh
   uv sync
   ```

2. **Start the FastAPI server**:
   ```sh
   uv run python -m app.main
   ```

3. **Development Mode (with auto-reload)**:
   Useful for development as it restarts the server when code changes.
   ```sh
   uv run uvicorn app.main:app --reload --port 3000
   ```

The server will start at **`http://localhost:3000`**.

### API Exploration

Once the server is running, you can access:
- **Interactive Documentation**: [http://localhost:3000/api/docs](http://localhost:3000/api/docs) (Swagger UI)
- **Alternative Documentation**: [http://localhost:3000/api/redoc](http://localhost:3000/api/redoc) (ReDoc)

### Running Tests

```sh
uv run pytest tests/
```

## Testing Structure

The test suite is located in the `tests/` directory and is split by functionality:
- `tests/test_auth.py`: Authentication endpoints (signup, login).
- `tests/test_leaderboard.py`: Leaderboard endpoints (GET, POST).
- `tests/conftest.py`: Shared fixtures (HTTP client).
