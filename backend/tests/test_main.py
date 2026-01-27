import pytest


@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["docs"] == "/api/docs"


@pytest.mark.asyncio
async def test_favicon(client):
    response = await client.get("/favicon.ico")
    assert response.status_code == 204
    assert response.text == ""
