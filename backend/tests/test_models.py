"""
Unit tests for SQLAlchemy models.
Tests model creation, relationships, and constraints.
"""
import pytest
from datetime import datetime, UTC
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.models import Base, User, SessionToken, LeaderboardEntry
from app import security


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh in-memory database for each test"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


class TestUserModel:
    """Tests for User model"""
    
    def test_create_user(self, db_session):
        """Test creating a user"""
        user = User(
            email="test@example.com",
            hashed_password=security.hash_password("password")
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert isinstance(user.id, uuid.UUID)
        assert user.email == "test@example.com"
        assert user.created_at is not None
    
    def test_user_email_unique_constraint(self, db_session):
        """Test that email must be unique"""
        user1 = User(
            email="duplicate@example.com",
            hashed_password=security.hash_password("password1")
        )
        db_session.add(user1)
        db_session.commit()
        
        user2 = User(
            email="duplicate@example.com",
            hashed_password=security.hash_password("password2")
        )
        db_session.add(user2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_user_default_created_at(self, db_session):
        """Test that created_at is set automatically"""
        before = datetime.now()  # Use naive datetime to match SQLAlchemy's default
        user = User(
            email="test@example.com",
            hashed_password=security.hash_password("password")
        )
        db_session.add(user)
        db_session.commit()
        after = datetime.now()
        
        assert user.created_at is not None
        assert before <= user.created_at <= after


class TestSessionTokenModel:
    """Tests for SessionToken model"""
    
    def test_create_session_token(self, db_session):
        """Test creating a session token"""
        user = User(
            email="test@example.com",
            hashed_password=security.hash_password("password")
        )
        db_session.add(user)
        db_session.commit()
        
        token = SessionToken(token="test_token_123", user_id=user.id)
        db_session.add(token)
        db_session.commit()
        
        assert token.token == "test_token_123"
        assert token.user_id == user.id
        assert token.created_at is not None
    
    def test_session_token_user_relationship(self, db_session):
        """Test relationship between SessionToken and User"""
        user = User(
            email="test@example.com",
            hashed_password=security.hash_password("password")
        )
        db_session.add(user)
        db_session.commit()
        
        token = SessionToken(token="test_token_123", user_id=user.id)
        db_session.add(token)
        db_session.commit()
        
        # Test forward relationship
        assert token.user.email == "test@example.com"
        
        # Test reverse relationship
        db_session.refresh(user)
        assert len(user.tokens) == 1
        assert user.tokens[0].token == "test_token_123"
    
    def test_cascade_delete_tokens(self, db_session):
        """Test that deleting user cascades to tokens"""
        user = User(
            email="test@example.com",
            hashed_password=security.hash_password("password")
        )
        db_session.add(user)
        db_session.commit()
        
        token1 = SessionToken(token="token1", user_id=user.id)
        token2 = SessionToken(token="token2", user_id=user.id)
        db_session.add_all([token1, token2])
        db_session.commit()
        
        user_id = user.id
        
        # Delete user
        db_session.delete(user)
        db_session.commit()
        
        # Tokens should be deleted
        remaining_tokens = db_session.query(SessionToken).filter(
            SessionToken.user_id == user_id
        ).count()
        assert remaining_tokens == 0


class TestLeaderboardEntryModel:
    """Tests for LeaderboardEntry model"""
    
    def test_create_leaderboard_entry(self, db_session):
        """Test creating a leaderboard entry"""
        entry = LeaderboardEntry(
            email="player@example.com",
            score=100,
            round=5
        )
        db_session.add(entry)
        db_session.commit()
        
        assert entry.id is not None
        assert entry.email == "player@example.com"
        assert entry.score == 100
        assert entry.round == 5
        assert entry.date is not None
    
    def test_leaderboard_entry_default_date(self, db_session):
        """Test that date is set automatically"""
        before = datetime.now()  # Use naive datetime to match SQLAlchemy's default
        entry = LeaderboardEntry(
            email="player@example.com",
            score=100,
            round=5
        )
        db_session.add(entry)
        db_session.commit()
        after = datetime.now()
        
        assert entry.date is not None
        assert before <= entry.date <= after
    
    def test_multiple_entries_same_email(self, db_session):
        """Test that same email can have multiple entries"""
        entry1 = LeaderboardEntry(
            email="player@example.com",
            score=100,
            round=5
        )
        entry2 = LeaderboardEntry(
            email="player@example.com",
            score=150,
            round=6
        )
        db_session.add_all([entry1, entry2])
        db_session.commit()
        
        entries = db_session.query(LeaderboardEntry).filter(
            LeaderboardEntry.email == "player@example.com"
        ).all()
        assert len(entries) == 2
    
    def test_leaderboard_entry_ordering(self, db_session):
        """Test querying leaderboard entries by score"""
        entries = [
            LeaderboardEntry(email="player1@example.com", score=100, round=5),
            LeaderboardEntry(email="player2@example.com", score=200, round=6),
            LeaderboardEntry(email="player3@example.com", score=50, round=3),
        ]
        db_session.add_all(entries)
        db_session.commit()
        
        # Query ordered by score descending
        ordered = db_session.query(LeaderboardEntry).order_by(
            LeaderboardEntry.score.desc()
        ).all()
        
        assert ordered[0].score == 200
        assert ordered[1].score == 100
        assert ordered[2].score == 50
