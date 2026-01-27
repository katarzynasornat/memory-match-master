import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_signup():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/signup", json={"email": "new@example.com", "password": "pass"})
    assert response.status_code == 201
    assert response.json()["user"]["email"] == "new@example.com"
    assert "token" in response.json()

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # First signup
        await ac.post("/auth/signup", json={"email": "login@example.com", "password": "password123"})
        # Then login
        response = await ac.post("/auth/login", json={"email": "login@example.com", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "login@example.com"

@pytest.mark.asyncio
async def test_get_leaderboard():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/leaderboard")
    assert response.status_code == 200
    assert len(response.json()) >= 3  # Based on initial mock data

@pytest.mark.asyncio
async def test_submit_score():
    email = "winner@example.com"
    token = f"mock-token-for-{email}"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Signup first to "exist"
        await ac.post("/auth/signup", json={"email": email, "password": "pass"})
        
        # Submit score
        response = await ac.post(
            "/leaderboard", 
            json={"email": email, "score": 1000, "round": 3},
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 201
    assert response.json()["message"] == "Score submitted successfully"

@pytest.mark.asyncio
async def test_submit_score_unauthorized():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/leaderboard", 
            json={"email": "hacker@example.com", "score": 9999, "round": 100}
        )
    assert response.status_code == 401
