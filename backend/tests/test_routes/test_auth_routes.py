import pytest


@pytest.mark.asyncio
async def test_register_user_route(client):
    payload = {
        "name": "Test User",
        "email": "route_test@example.com",
        "password": "strongpassword"
    }
    response = await client.post("/register", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data


@pytest.mark.asyncio
async def test_login_user_route(client):
    # Сначала регистрируем
    reg_payload = {"name": "Login Test", "email": "login@test.com", "password": "123"}
    await client.post("/register", json=reg_payload)

    # Пытаемся залогиниться
    login_payload = {"email": "login@test.com", "password": "123"}
    response = await client.post("/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"