import pytest


@pytest.mark.asyncio
async def test_signup(client):
    response = await client.post(
        "/auth/signup", json={"email": "new_refactored@example.com", "password": "pass"}
    )
    assert response.status_code == 201
    assert response.json()["user"]["email"] == "new_refactored@example.com"
    assert "token" in response.json()


@pytest.mark.asyncio
async def test_login(client):
    # First signup
    await client.post(
        "/auth/signup",
        json={"email": "login_refactored@example.com", "password": "password123"},
    )
    # Then login
    response = await client.post(
        "/auth/login",
        json={"email": "login_refactored@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "login_refactored@example.com"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    response = await client.post(
        "/auth/login", json={"email": "nonexistent@example.com", "password": "wrong"}
    )
    assert response.status_code == 401
