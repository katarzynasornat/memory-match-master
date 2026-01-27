"""
Integration tests for database operations.
Tests database initialization, connections, and data integrity.
"""
import pytest
import os
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, LeaderboardEntry, SessionToken
from app import security


@pytest.mark.asyncio
async def test_database_file_exists_during_test():
    """Test that the database file is created"""
    assert os.path.exists("/tmp/test_integration.db")


@pytest.mark.asyncio
async def test_all_tables_created(setup_db):
    """Test that all required tables are created"""
    engine = setup_db  # Get engine from fixture
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    assert "users" in tables
    assert "session_tokens" in tables
    assert "leaderboard_entries" in tables


@pytest.mark.asyncio
async def test_prepopulated_data_exists(client):
    """Test that database is pre-populated with test data"""
    # Check leaderboard entries
    response = await client.get("/leaderboard")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3  # We pre-populate with 3 entries
    
    # Verify specific entries
    emails = [entry["email"] for entry in data]
    assert "pro_player@example.com" in emails
    assert "neon_god@example.com" in emails
    assert "gamer123@example.com" in emails


@pytest.mark.asyncio
async def test_user_session_token_relationship(setup_db):
    """Test the foreign key relationship between User and SessionToken"""
    engine = setup_db  # Get engine from fixture
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Create a user
        user = User(
            email="relationship_test@example.com",
            hashed_password=security.hash_password("password")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create a session token for this user
        token = SessionToken(token="test_token_123", user_id=user.id)
        db.add(token)
        db.commit()
        
        # Verify relationship
        db.refresh(user)
        assert len(user.tokens) == 1
        assert user.tokens[0].token == "test_token_123"
        
        # Verify reverse relationship
        db.refresh(token)
        assert token.user.email == "relationship_test@example.com"
    finally:
        db.close()


@pytest.mark.asyncio
async def test_cascade_delete_tokens_on_user_delete(setup_db):
    """Test that deleting a user cascades to delete their tokens"""
    engine = setup_db  # Get engine from fixture
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Create user with tokens
        user = User(
            email="cascade_test@example.com",
            hashed_password=security.hash_password("password")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Add multiple tokens
        token1 = SessionToken(token="token1", user_id=user.id)
        token2 = SessionToken(token="token2", user_id=user.id)
        db.add_all([token1, token2])
        db.commit()
        
        user_id = user.id
        
        # Verify tokens exist
        tokens_before = db.query(SessionToken).filter(SessionToken.user_id == user_id).count()
        assert tokens_before == 2
        
        # Delete user
        db.delete(user)
        db.commit()
        
        # Verify tokens are also deleted (cascade)
        tokens_after = db.query(SessionToken).filter(SessionToken.user_id == user_id).count()
        assert tokens_after == 0
    finally:
        db.close()


@pytest.mark.asyncio
async def test_database_transaction_rollback(setup_db):
    """Test that database transactions can be rolled back"""
    engine = setup_db  # Get engine from fixture
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Count initial users
        initial_count = db.query(User).count()
        
        # Add a user but don't commit
        user = User(
            email="rollback_test@example.com",
            hashed_password=security.hash_password("password")
        )
        db.add(user)
        db.flush()  # Flush to database but don't commit
        
        # Rollback
        db.rollback()
        
        # Verify user was not persisted
        final_count = db.query(User).count()
        assert final_count == initial_count
    finally:
        db.close()


@pytest.mark.asyncio
async def test_unique_email_constraint(setup_db):
    """Test that email uniqueness is enforced at database level"""
    engine = setup_db  # Get engine from fixture
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Create first user
        user1 = User(
            email="unique@example.com",
            hashed_password=security.hash_password("password1")
        )
        db.add(user1)
        db.commit()
        
        # Try to create second user with same email
        user2 = User(
            email="unique@example.com",
            hashed_password=security.hash_password("password2")
        )
        db.add(user2)
        
        # This should raise an integrity error
        with pytest.raises(Exception):  # SQLAlchemy will raise IntegrityError
            db.commit()
    finally:
        db.rollback()
        db.close()


@pytest.mark.asyncio
async def test_leaderboard_entry_persistence(authenticated_user, client):
    """Test that leaderboard entries persist across multiple queries"""
    token = authenticated_user["token"]
    email = authenticated_user["email"]
    score = 777
    
    # Submit score
    await client.post(
        "/leaderboard",
        json={"email": email, "score": score, "round": 7},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Query leaderboard multiple times
    for _ in range(3):
        response = await client.get("/leaderboard")
        data = response.json()
        our_entry = next((e for e in data if e["email"] == email.lower()), None)
        assert our_entry is not None
        assert our_entry["score"] == score


@pytest.mark.asyncio
async def test_database_connection_handling(setup_db):
    """Test that database connections are properly managed"""
    engine = setup_db  # Get engine from fixture
    SessionLocal = sessionmaker(bind=engine)
    
    # Create multiple sessions
    sessions = []
    for _ in range(5):
        db = SessionLocal()
        sessions.append(db)
        # Perform a simple query
        db.query(User).count()
    
    # Close all sessions
    for db in sessions:
        db.close()
    
    # Should be able to create new session after closing
    db = SessionLocal()
    count = db.query(User).count()
    assert count >= 0
    db.close()
