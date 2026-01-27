import pytest


@pytest.mark.asyncio
async def test_get_leaderboard(client):
    response = await client.get("/leaderboard")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 3


@pytest.mark.asyncio
async def test_submit_score(client):
    email = "winner_refactored@example.com"

    # Signup first to "exist" and get token
    signup_resp = await client.post(
        "/auth/signup", json={"email": email, "password": "pass"}
    )
    token = signup_resp.json()["token"]

    # Submit score
    response = await client.post(
        "/leaderboard",
        json={"email": email, "score": 1000, "round": 3},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["message"] == "Score submitted successfully"


@pytest.mark.asyncio
async def test_submit_score_unauthorized(client):
    response = await client.post(
        "/leaderboard",
        json={"email": "hacker@example.com", "score": 9999, "round": 100},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_submit_score_forbidden(client):
    # Try to submit score for another user
    signup_resp = await client.post(
        "/auth/signup", json={"email": "user1@example.com", "password": "pass"}
    )
    token = signup_resp.json()["token"]

    response = await client.post(
        "/leaderboard",
        json={"email": "user2@example.com", "score": 100, "round": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
