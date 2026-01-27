"""
Integration tests for authentication endpoints.
Tests the full authentication flow with a real SQLite database.
"""
import pytest


@pytest.mark.asyncio
async def test_signup_creates_user_in_database(client):
    """Test that signup creates a user in the database"""
    email = "newuser@example.com"
    password = "mypassword123"
    
    response = await client.post(
        "/auth/signup",
        json={"email": email, "password": password}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "user" in data
    assert "token" in data
    assert data["user"]["email"] == email.lower()
    assert "id" in data["user"]
    assert data["token"].startswith("mt_")


@pytest.mark.asyncio
async def test_signup_duplicate_user_fails(client):
    """Test that signing up with an existing email fails"""
    email = "duplicate@example.com"
    password = "password123"
    
    # First signup should succeed
    response1 = await client.post(
        "/auth/signup",
        json={"email": email, "password": password}
    )
    assert response1.status_code == 201
    
    # Second signup with same email should fail
    response2 = await client.post(
        "/auth/signup",
        json={"email": email, "password": password}
    )
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"].lower()


@pytest.mark.asyncio
async def test_signup_case_insensitive_email(client):
    """Test that email is stored in lowercase"""
    email = "CaseSensitive@Example.COM"
    password = "password123"
    
    response = await client.post(
        "/auth/signup",
        json={"email": email, "password": password}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["email"] == email.lower()


@pytest.mark.asyncio
async def test_login_with_valid_credentials(client):
    """Test login with valid credentials"""
    email = "loginuser@example.com"
    password = "securepass123"
    
    # First signup
    await client.post(
        "/auth/signup",
        json={"email": email, "password": password}
    )
    
    # Then login
    response = await client.post(
        "/auth/login",
        json={"email": email, "password": password}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert "token" in data
    assert data["user"]["email"] == email.lower()
    assert data["token"].startswith("mt_")


@pytest.mark.asyncio
async def test_login_with_invalid_password(client):
    """Test login with wrong password"""
    email = "loginuser2@example.com"
    password = "correctpass"
    
    # Signup
    await client.post(
        "/auth/signup",
        json={"email": email, "password": password}
    )
    
    # Login with wrong password
    response = await client.post(
        "/auth/login",
        json={"email": email, "password": "wrongpass"}
    )
    
    assert response.status_code == 401
    assert "invalid credentials" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_with_nonexistent_user(client):
    """Test login with email that doesn't exist"""
    response = await client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "anypass"}
    )
    
    assert response.status_code == 401
    assert "invalid credentials" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_case_insensitive(client):
    """Test that login works with different email casing"""
    email = "CaseTest@Example.Com"
    password = "password123"
    
    # Signup with mixed case
    await client.post(
        "/auth/signup",
        json={"email": email, "password": password}
    )
    
    # Login with different casing
    response = await client.post(
        "/auth/login",
        json={"email": email.upper(), "password": password}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == email.lower()


@pytest.mark.asyncio
async def test_token_persists_across_requests(authenticated_user, client):
    """Test that token works for authenticated requests"""
    token = authenticated_user["token"]
    email = authenticated_user["email"]
    
    # Use token to submit a score (requires authentication)
    response = await client.post(
        "/leaderboard",
        json={"email": email, "score": 100, "round": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_multiple_logins_generate_different_tokens(client):
    """Test that each login generates a new token"""
    email = "multilogin@example.com"
    password = "password123"
    
    # Signup
    await client.post(
        "/auth/signup",
        json={"email": email, "password": password}
    )
    
    # Login twice
    response1 = await client.post(
        "/auth/login",
        json={"email": email, "password": password}
    )
    response2 = await client.post(
        "/auth/login",
        json={"email": email, "password": password}
    )
    
    token1 = response1.json()["token"]
    token2 = response2.json()["token"]
    
    # Tokens should be different
    assert token1 != token2
    
    # Both tokens should work
    response = await client.post(
        "/leaderboard",
        json={"email": email, "score": 50, "round": 3},
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 201
    
    response = await client.post(
        "/leaderboard",
        json={"email": email, "score": 60, "round": 4},
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 201
