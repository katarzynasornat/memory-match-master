# Integration Tests

This directory contains integration tests for the Memory Match backend API. These tests use a **file-based SQLite database** to verify end-to-end functionality with real database persistence.

## Purpose

Integration tests verify that different components of the application work together correctly:
- API endpoints with database operations
- Authentication flow with token persistence
- Leaderboard functionality with data persistence
- Database relationships and constraints

## Differences from Unit Tests

| Aspect | Unit Tests (`tests/`) | Integration Tests (`tests_integration/`) |
|--------|----------------------|------------------------------------------|
| Database | In-memory SQLite | File-based SQLite (`test_integration.db`) |
| Scope | Individual components | End-to-end workflows |
| Speed | Faster | Slower (file I/O) |
| Isolation | High | Medium |

## Running Integration Tests

### Run integration tests only:
```bash
make test-integration
```

Or using `uv` directly:
```bash
uv run pytest tests_integration/ -v
```

### Run all tests (unit + integration):
```bash
make test-all
```

### Run specific test file:
```bash
uv run pytest tests_integration/test_auth_integration.py -v
```

### Run specific test:
```bash
uv run pytest tests_integration/test_auth_integration.py::test_signup_creates_user_in_database -v
```

## Test Structure

- **`conftest.py`**: Pytest configuration with fixtures for database setup, test client, and authenticated users
- **`test_auth_integration.py`**: Authentication flow tests (signup, login, tokens)
- **`test_leaderboard_integration.py`**: Leaderboard functionality tests (submit, retrieve, ordering)
- **`test_database_integration.py`**: Database operations tests (relationships, constraints, transactions)

## Test Database

- **File**: `test_integration.db` (created in backend directory)
- **Lifecycle**: Created fresh for each test, cleaned up after test completes
- **Pre-populated data**: Each test starts with mock leaderboard entries and a test user

## Fixtures

### `setup_db` (autouse)
Automatically creates a fresh database for each test and cleans up afterward.

### `client`
Provides an async HTTP client for making API requests.

### `authenticated_user`
Creates and authenticates a test user, returns email, password, token, and user_id.

## Best Practices

1. **Use fixtures**: Leverage `authenticated_user` fixture for tests requiring authentication
2. **Test persistence**: Verify data persists across multiple requests
3. **Clean state**: Each test gets a fresh database (no shared state)
4. **Real workflows**: Test complete user flows, not just individual endpoints
5. **Follow AGENTS.md**: Use `uv` for running tests as specified in project guidelines
