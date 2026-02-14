import pytest
from unittest.mock import patch


@pytest.mark.asyncio
async def test_contact_form_success(client):
    payload = {
        "name": "Ivan",
        "email": "ivan@test.com",
        "subject": "Help",
        "message": "I have a question"
    }

    # Мокаем функцию send_to_telegram, чтобы она всегда возвращала True
    with patch("app.routes.contact.send_to_telegram", return_value=True):
        response = await client.post("/contacts/contact", json=payload)

    assert response.status_code == 200
    assert response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_contact_form_invalid_email(client):
    payload = {
        "name": "Ivan",
        "email": "not-an-email",  # Pydantic должен это поймать
        "subject": "Help",
        "message": "Text"
    }
    response = await client.post("/contacts/contact", json=payload)
    assert response.status_code == 422  # Unprocessable Entity