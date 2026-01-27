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
make install           # Install dependencies
make dev               # Start development server (hot-reload)
make run               # Start production server
make test              # Run unit tests
make test-integration  # Run integration tests
make test-all          # Run all tests (unit + integration)
make lint              # Run lint checks
make format            # Format code
make migrate           # Run database migrations
make revision MSG="description" # Create a new migration
```

## Database Configuration

This project uses SQLAlchemy with Alembic for database management. By default, it uses an SQLite database file (`game.db`) in the root directory.

### Environment Variables
For production, you can configure a PostgreSQL database by setting the `DATABASE_URL` environment variable:
```sh
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
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

The project includes both **unit tests** and **integration tests**:

```sh
# Run all tests (unit + integration)
make test-all

# Run only unit tests
make test

# Run only integration tests
make test-integration
```

Or using `uv` directly:
```sh
# All tests
uv run pytest tests/ tests_integration/

# Unit tests only
uv run pytest tests/

# Integration tests only
uv run pytest tests_integration/
```

## Testing Structure

### Unit Tests (`tests/`)
Fast, in-memory tests for individual components:
- `tests/test_auth.py`: Authentication endpoints (signup, login)
- `tests/test_leaderboard.py`: Leaderboard endpoints (GET, POST)
- `tests/conftest.py`: Shared fixtures (HTTP client, in-memory database)

### Integration Tests (`tests_integration/`)
End-to-end tests using file-based SQLite to verify complete workflows:
- `tests_integration/test_auth_integration.py`: Full authentication flow (9 tests)
- `tests_integration/test_leaderboard_integration.py`: Leaderboard persistence and ordering (10 tests)
- `tests_integration/test_database_integration.py`: Database operations and relationships (9 tests)
- `tests_integration/conftest.py`: Test fixtures with file-based database setup
- `tests_integration/README.md`: Detailed integration test documentation

**Total: 38 tests** (10 unit + 28 integration)
