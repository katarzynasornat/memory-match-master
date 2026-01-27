"""
Integration tests for leaderboard endpoints.
Tests the full leaderboard flow with a real SQLite database.
"""
import pytest


@pytest.mark.asyncio
async def test_get_leaderboard_returns_top_entries(client):
    """Test that GET /leaderboard returns entries ordered by score"""
    response = await client.get("/leaderboard")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  # We pre-populate with 3 entries
    
    # Verify ordering (highest score first)
    scores = [entry["score"] for entry in data]
    assert scores == sorted(scores, reverse=True)


@pytest.mark.asyncio
async def test_get_leaderboard_limits_to_10_entries(client, authenticated_user):
    """Test that leaderboard returns at most 10 entries"""
    token = authenticated_user["token"]
    email = authenticated_user["email"]
    
    # Add 15 more entries
    for i in range(15):
        await client.post(
            "/leaderboard",
            json={"email": email, "score": i * 10, "round": i},
            headers={"Authorization": f"Bearer {token}"}
        )
    
    response = await client.get("/leaderboard")
    data = response.json()
    
    assert len(data) <= 10


@pytest.mark.asyncio
async def test_submit_score_requires_authentication(client):
    """Test that submitting a score without auth fails"""
    response = await client.post(
        "/leaderboard",
        json={"email": "hacker@example.com", "score": 9999, "round": 100}
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_submit_score_with_valid_auth(authenticated_user, client):
    """Test submitting a score with valid authentication"""
    token = authenticated_user["token"]
    email = authenticated_user["email"]
    
    response = await client.post(
        "/leaderboard",
        json={"email": email, "score": 85, "round": 6},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    assert response.json()["message"] == "Score submitted successfully"


@pytest.mark.asyncio
async def test_submit_score_persists_to_database(authenticated_user, client):
    """Test that submitted score appears in leaderboard"""
    token = authenticated_user["token"]
    email = authenticated_user["email"]
    score = 999
    
    # Submit score
    await client.post(
        "/leaderboard",
        json={"email": email, "score": score, "round": 10},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Verify it appears in leaderboard
    response = await client.get("/leaderboard")
    data = response.json()
    
    # Find our entry
    our_entry = next((e for e in data if e["email"] == email.lower()), None)
    assert our_entry is not None
    assert our_entry["score"] == score


@pytest.mark.asyncio
async def test_submit_score_for_another_user_fails(authenticated_user, client):
    """Test that user cannot submit score for another user"""
    token = authenticated_user["token"]
    
    response = await client.post(
        "/leaderboard",
        json={"email": "otheruser@example.com", "score": 100, "round": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403
    assert "cannot submit score for another user" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_submit_multiple_scores_same_user(authenticated_user, client):
    """Test that a user can submit multiple scores"""
    token = authenticated_user["token"]
    email = authenticated_user["email"]
    
    # Submit first score
    response1 = await client.post(
        "/leaderboard",
        json={"email": email, "score": 50, "round": 3},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response1.status_code == 201
    
    # Submit second score
    response2 = await client.post(
        "/leaderboard",
        json={"email": email, "score": 75, "round": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response2.status_code == 201
    
    # Both should appear in leaderboard
    response = await client.get("/leaderboard")
    data = response.json()
    user_entries = [e for e in data if e["email"] == email.lower()]
    assert len(user_entries) >= 2


@pytest.mark.asyncio
async def test_leaderboard_ordering_after_new_submission(authenticated_user, client):
    """Test that leaderboard maintains correct ordering after new submissions"""
    token = authenticated_user["token"]
    email = authenticated_user["email"]
    
    # Submit a very high score
    high_score = 10000
    await client.post(
        "/leaderboard",
        json={"email": email, "score": high_score, "round": 10},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Get leaderboard
    response = await client.get("/leaderboard")
    data = response.json()
    
    # Our high score should be first
    assert data[0]["score"] == high_score
    assert data[0]["email"] == email.lower()


@pytest.mark.asyncio
async def test_submit_score_case_insensitive_email(authenticated_user, client):
    """Test that score submission handles email case-insensitively"""
    token = authenticated_user["token"]
    email = authenticated_user["email"]
    
    # Submit with different casing
    response = await client.post(
        "/leaderboard",
        json={"email": email.upper(), "score": 42, "round": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_leaderboard_entry_has_timestamp(authenticated_user, client):
    """Test that leaderboard entries include timestamp"""
    token = authenticated_user["token"]
    email = authenticated_user["email"]
    
    # Submit score
    await client.post(
        "/leaderboard",
        json={"email": email, "score": 123, "round": 4},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Get leaderboard
    response = await client.get("/leaderboard")
    data = response.json()
    
    # Find our entry and check for date field
    our_entry = next((e for e in data if e["email"] == email.lower()), None)
    assert our_entry is not None
    assert "date" in our_entry
    assert our_entry["date"] is not None
