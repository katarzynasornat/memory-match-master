import os

# Set TESTING env var before importing app.main to prevent database.init_db() execution
os.environ["TESTING"] = "1"

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

from sqlalchemy.pool import StaticPool

# Use in-memory SQLite for testing with StaticPool to keep it across connections
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

from datetime import datetime, UTC
from app.models import LeaderboardEntry

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    # Pre-populate leaderboard for tests
    db = TestingSessionLocal()
    mock_entries = [
        LeaderboardEntry(email="pro_player@example.com", score=48, round=5, date=datetime.now(UTC)),
        LeaderboardEntry(email="neon_god@example.com", score=45, round=5, date=datetime.now(UTC)),
        LeaderboardEntry(email="gamer123@example.com", score=38, round=4, date=datetime.now(UTC)),
    ]
    db.add_all(mock_entries)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
