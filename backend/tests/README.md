# Backend Tests

This directory contains **unit tests** for the Memory Match backend. Unit tests check individual pieces of code in isolation to ensure they work correctly.

## What's Inside

### Test Files (51 tests total)

#### Security Tests (`test_security.py`) - 9 tests
Tests password hashing and verification:
- Passwords are hashed securely (not stored in plain text)
- Same password creates different hashes (for security)
- Correct passwords verify successfully
- Wrong passwords are rejected
- Special characters and unicode work correctly

#### Schema Tests (`test_schemas.py`) - 23 tests
Tests data validation using Pydantic:
- Email addresses must be valid format
- Passwords must be at least 4 characters
- Required fields cannot be missing
- Invalid data is rejected with clear error messages

#### Model Tests (`test_models.py`) - 13 tests
Tests database models using SQLAlchemy:
- Users are created with unique IDs
- Email addresses must be unique (no duplicates)
- Timestamps are set automatically
- Relationships work (users have tokens)
- Deleting a user also deletes their tokens (cascade)

#### API Tests
- `test_auth.py` (3 tests) - Signup and login endpoints
- `test_leaderboard.py` (5 tests) - Leaderboard GET/POST endpoints
- `test_main.py` (2 tests) - Root and health check endpoints

### Configuration (`conftest.py`)
Sets up test fixtures:
- Creates an in-memory database for each test (fast and isolated)
- Provides an HTTP client for testing API endpoints
- Pre-populates test data (mock leaderboard entries)

## How to Run

```bash
# Run all unit tests
make test

# Or using uv directly
uv run pytest tests/

# Run a specific test file
uv run pytest tests/test_security.py -v

# Run tests matching a pattern
uv run pytest -k "password" -v
```

## Why Unit Tests?

Unit tests are **fast** (run in ~8 seconds) and help you:
1. **Catch bugs early** - Find problems before they reach production
2. **Refactor safely** - Change code with confidence it still works
3. **Document behavior** - Tests show how code is supposed to work
4. **Debug faster** - Failing tests pinpoint exactly what broke

## Unit Tests vs Integration Tests

- **Unit Tests** (this directory): Test individual functions/classes in isolation using in-memory database
- **Integration Tests** (`tests_integration/`): Test complete workflows using a real database file

Both are important! Unit tests are fast and precise, while integration tests ensure everything works together.

## Test Results

All 51 unit tests pass:
- ✅ 9 security tests
- ✅ 23 schema validation tests
- ✅ 13 database model tests
- ✅ 3 auth endpoint tests
- ✅ 5 leaderboard endpoint tests
- ✅ 2 main app tests

**Total runtime:** ~8 seconds
