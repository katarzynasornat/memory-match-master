import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from . import models, security
from .models import Base, LeaderboardEntry, User
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Default to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./game.db")

# Use check_same_thread=False only for SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Only for initial creation if not using Alembic right away
    Base.metadata.create_all(bind=engine)
    
    # Pre-populate leaderboard if empty
    db = SessionLocal()
    if db.query(LeaderboardEntry).count() == 0:
        mock_entries = [
            LeaderboardEntry(email="pro_player@example.com", score=48, round=5, date=datetime.now()),
            LeaderboardEntry(email="neon_god@example.com", score=45, round=5, date=datetime.now()),
            LeaderboardEntry(email="gamer123@example.com", score=38, round=4, date=datetime.now()),
            LeaderboardEntry(email="memory_master@example.com", score=32, round=3, date=datetime.now()),
            LeaderboardEntry(email="arcade_king@example.com", score=28, round=3, date=datetime.now()),
            LeaderboardEntry(email="quick_fingers@example.com", score=22, round=2, date=datetime.now()),
            LeaderboardEntry(email="chill_player@example.com", score=18, round=2, date=datetime.now()),
            LeaderboardEntry(email="newbie@example.com", score=12, round=1, date=datetime.now()),
            LeaderboardEntry(email="casual@example.com", score=8, round=1, date=datetime.now()),
            LeaderboardEntry(email="tester@example.com", score=5, round=1, date=datetime.now()),
        ]
        db.add_all(mock_entries)
        db.commit()

    # Pre-populate test user if none exist
    if db.query(User).count() == 0:
        test_user = User(
            email="tester@example.com",
            hashed_password=security.hash_password("password123")
        )
        db.add(test_user)
        db.commit()

    db.close()
