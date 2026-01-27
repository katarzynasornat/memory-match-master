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

The backend has **79 comprehensive tests** to ensure everything works correctly. Tests are split into two types:

```bash
# Run all tests (recommended before committing code)
make test-all

# Run only unit tests (fast, for quick feedback)
make test

# Run only integration tests (slower, tests full workflows)
make test-integration
```

Or using `uv` directly:
```bash
# All tests
uv run pytest tests/ tests_integration/

# Unit tests only
uv run pytest tests/

# Integration tests only
uv run pytest tests_integration/
```

## Testing Structure

### What Are Tests?
Tests are automated checks that verify your code works correctly. Think of them like a checklist that runs automatically to catch bugs before they reach users.

### Unit Tests (`tests/`) - 51 tests
**Purpose:** Test individual pieces of code in isolation (like testing a single LEGO brick)

**What's tested:**
- **Security** (`test_security.py` - 9 tests)
  - Password hashing works correctly
  - Passwords are verified properly
  - Special characters and unicode are handled
  
- **Data Validation** (`test_schemas.py` - 23 tests)
  - Email addresses are valid
  - Passwords meet minimum length
  - Required fields are present
  
- **Database Models** (`test_models.py` - 13 tests)
  - Users are created correctly
  - Relationships between users and tokens work
  - Unique email constraint is enforced
  
- **API Endpoints** (`test_auth.py`, `test_leaderboard.py`, `test_main.py` - 10 tests)
  - Signup and login work
  - Leaderboard retrieval and submission work
  - Health checks respond correctly

**Speed:** Fast (~8 seconds) - uses in-memory database

### Integration Tests (`tests_integration/`) - 28 tests
**Purpose:** Test complete workflows from start to finish (like testing a fully assembled LEGO set)

**What's tested:**
- **Full Authentication Flow** (`test_auth_integration.py` - 9 tests)
  - Users can sign up and data is saved to database
  - Login generates persistent tokens
  - Duplicate emails are prevented
  
- **Complete Leaderboard Workflow** (`test_leaderboard_integration.py` - 10 tests)
  - Scores are saved and retrieved correctly
  - Leaderboard is ordered by score
  - Users can only submit their own scores
  
- **Database Operations** (`test_database_integration.py` - 9 tests)
  - All tables are created properly
  - Deleting a user also deletes their tokens
  - Transactions can be rolled back

**Speed:** Slower (~15 seconds) - uses real file-based database

**Key Difference:** Integration tests use a real SQLite database file (`/tmp/test_integration.db`) instead of in-memory, so they test the full database behavior including file operations and persistence.

### Why Both Types?
- **Unit tests** are fast and help you quickly find which specific function is broken
- **Integration tests** are thorough and ensure all the pieces work together correctly
- Together, they give you confidence that your code works both in isolation and as a complete system

### Test Results
All 79 tests pass with zero warnings:
- ✅ 51 unit tests (8 seconds)
- ✅ 28 integration tests (15 seconds)
- ✅ Total: 79 tests in ~23 seconds

### For Developers
Before committing your changes, always run `make test-all` to ensure you haven't broken anything. If a test fails, it will tell you exactly what went wrong and where.
