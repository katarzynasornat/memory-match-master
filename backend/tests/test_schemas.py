"""
Unit tests for Pydantic schemas.
Tests validation and serialization of data models.
"""
import pytest
from pydantic import ValidationError
from datetime import datetime, UTC
import uuid
from app import schemas


class TestUserSchemas:
    """Tests for User-related schemas"""
    
    def test_user_create_valid(self):
        """Test creating valid UserCreate schema"""
        user = schemas.UserCreate(email="test@example.com", password="password123")
        assert user.email == "test@example.com"
        assert user.password == "password123"
    
    def test_user_create_invalid_email(self):
        """Test that invalid email raises validation error"""
        with pytest.raises(ValidationError):
            schemas.UserCreate(email="not-an-email", password="password123")
    
    def test_user_create_password_too_short(self):
        """Test that password shorter than 4 characters raises error"""
        with pytest.raises(ValidationError):
            schemas.UserCreate(email="test@example.com", password="abc")
    
    def test_user_create_password_minimum_length(self):
        """Test that password with exactly 4 characters is valid"""
        user = schemas.UserCreate(email="test@example.com", password="abcd")
        assert user.password == "abcd"
    
    def test_user_schema_with_uuid(self):
        """Test User schema with UUID"""
        user_id = uuid.uuid4()
        user = schemas.User(email="test@example.com", id=user_id)
        assert user.id == user_id
        assert user.email == "test@example.com"


class TestLeaderboardSchemas:
    """Tests for Leaderboard-related schemas"""
    
    def test_leaderboard_entry_create_valid(self):
        """Test creating valid LeaderboardEntryCreate"""
        entry = schemas.LeaderboardEntryCreate(
            email="player@example.com",
            score=100,
            round=5
        )
        assert entry.email == "player@example.com"
        assert entry.score == 100
        assert entry.round == 5
        assert entry.date is None  # Optional field
    
    def test_leaderboard_entry_create_with_date(self):
        """Test creating LeaderboardEntryCreate with date"""
        now = datetime.now(UTC)
        entry = schemas.LeaderboardEntryCreate(
            email="player@example.com",
            score=100,
            round=5,
            date=now
        )
        assert entry.date == now
    
    def test_leaderboard_entry_invalid_email(self):
        """Test that invalid email raises validation error"""
        with pytest.raises(ValidationError):
            schemas.LeaderboardEntryCreate(
                email="invalid-email",
                score=100,
                round=5
            )
    
    def test_leaderboard_entry_negative_score(self):
        """Test that negative score is accepted (no validation rule against it)"""
        # Note: If you want to prevent negative scores, add validation to schema
        entry = schemas.LeaderboardEntryCreate(
            email="player@example.com",
            score=-10,
            round=1
        )
        assert entry.score == -10
    
    def test_leaderboard_entry_zero_round(self):
        """Test that zero round is accepted"""
        entry = schemas.LeaderboardEntryCreate(
            email="player@example.com",
            score=50,
            round=0
        )
        assert entry.round == 0
    
    def test_leaderboard_entry_missing_required_fields(self):
        """Test that missing required fields raises error"""
        with pytest.raises(ValidationError):
            schemas.LeaderboardEntryCreate(email="player@example.com")
    
    def test_leaderboard_entry_response_schema(self):
        """Test LeaderboardEntry response schema"""
        now = datetime.now(UTC)
        entry = schemas.LeaderboardEntry(
            email="player@example.com",
            score=100,
            round=5,
            date=now
        )
        assert entry.email == "player@example.com"
        assert entry.score == 100
        assert entry.round == 5
        assert entry.date == now


class TestAuthResponse:
    """Tests for AuthResponse schema"""
    
    def test_auth_response_valid(self):
        """Test creating valid AuthResponse"""
        user_id = uuid.uuid4()
        user = schemas.User(email="test@example.com", id=user_id)
        auth_response = schemas.AuthResponse(user=user, token="test_token_123")
        
        assert auth_response.user.email == "test@example.com"
        assert auth_response.user.id == user_id
        assert auth_response.token == "test_token_123"
    
    def test_auth_response_missing_token(self):
        """Test that missing token raises error"""
        user_id = uuid.uuid4()
        user = schemas.User(email="test@example.com", id=user_id)
        
        with pytest.raises(ValidationError):
            schemas.AuthResponse(user=user)


class TestEmailValidation:
    """Tests for email validation across schemas"""
    
    @pytest.mark.parametrize("email", [
        "valid@example.com",
        "user.name@example.com",
        "user+tag@example.co.uk",
        "123@example.com",
    ])
    def test_valid_emails(self, email):
        """Test that various valid email formats are accepted"""
        user = schemas.UserCreate(email=email, password="password")
        assert user.email == email
    
    @pytest.mark.parametrize("email", [
        "invalid",
        "@example.com",
        "user@",
        "user name@example.com",
        "user@example",
    ])
    def test_invalid_emails(self, email):
        """Test that invalid email formats are rejected"""
        with pytest.raises(ValidationError):
            schemas.UserCreate(email=email, password="password")
