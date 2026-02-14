import pytest
from unittest.mock import patch

"""
Тестирование формы обратной связи:
- POST /contacts/contact (Success): Проверка отправки данных с использованием Mock для Telegram API (изолируем тесты от внешних сервисов).
- POST /contacts/contact (Validation Error): Проверка встроенной валидации Pydantic. Ожидаем ошибку 422 при некорректном формате email.
"""

@pytest.mark.asyncio
async def test_contact_form_success(client):
    payload = {
        "name": "Ivan",
        "email": "ivan@test.com",
        "subject": "Help",
        "message": "I have a question"
    }

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