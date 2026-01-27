import pytest
import os
from pathlib import Path

# CRITICAL: Set this BEFORE importing app to prevent init_db() from running
os.environ["TESTING"] = "1"

from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base, LeaderboardEntry, User
from app import security
from datetime import datetime, UTC

# Use file-based SQLite for integration tests to simulate real database behavior
# Use /tmp directory to ensure we have write permissions
TEST_DB_PATH = "/tmp/test_integration.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """Create fresh database for each test and clean up afterward"""
    # Remove existing test database and related files if they exist
    for file_path in [TEST_DB_PATH, f"{TEST_DB_PATH}-journal", f"{TEST_DB_PATH}-wal", f"{TEST_DB_PATH}-shm"]:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # Ignore errors during cleanup
    
    # Create a fresh engine for this test
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Override the database dependency
    def override_get_db():
        """Override database dependency for integration tests"""
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Pre-populate with some test data
    db = TestingSessionLocal()
    try:
        # Add mock leaderboard entries
        mock_entries = [
            LeaderboardEntry(
                email="pro_player@example.com",
                score=48,
                round=5,
                date=datetime.now(UTC)
            ),
            LeaderboardEntry(
                email="neon_god@example.com",
                score=45,
                round=5,
                date=datetime.now(UTC)
            ),
            LeaderboardEntry(
                email="gamer123@example.com",
                score=38,
                round=4,
                date=datetime.now(UTC)
            ),
        ]
        db.add_all(mock_entries)
        
        # Add a test user
        test_user = User(
            email="testuser@example.com",
            hashed_password=security.hash_password("testpass123")
        )
        db.add(test_user)
        db.commit()
    finally:
        db.close()
    
    yield engine  # Provide the engine to tests that need it
    
    # Cleanup: close all connections, drop tables, and remove database files
    engine.dispose()  # Close all connections in the pool
    Base.metadata.drop_all(bind=engine)
    
    # Remove all database files
    for file_path in [TEST_DB_PATH, f"{TEST_DB_PATH}-journal", f"{TEST_DB_PATH}-wal", f"{TEST_DB_PATH}-shm"]:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # Ignore errors during cleanup


@pytest.fixture
async def client():
    """Async HTTP client for testing the API"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def authenticated_user(client):
    """Create and authenticate a test user, return email and token"""
    email = "authuser@example.com"
    password = "securepass123"
    
    # Signup
    response = await client.post(
        "/auth/signup",
        json={"email": email, "password": password}
    )
    assert response.status_code == 201
    data = response.json()
    
    return {
        "email": email,
        "password": password,
        "token": data["token"],
        "user_id": data["user"]["id"]
    }
