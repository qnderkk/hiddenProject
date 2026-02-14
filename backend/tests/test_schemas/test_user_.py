import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate, UserResponse

"""
Тестирование схем валидации пользователя (Pydantic):
- UserCreate: проверка успешного создания объекта при корректных данных.
- Валидация Email: проверка выброса ValidationError при некорректном формате почты.
- UserResponse: тестирование механизма преобразования ORM-моделей в DTO (Data Transfer Object).
"""

def test_user_create_success():
    payload = {"name": "Ivan", "email": "ivan@example.com", "password": "securepassword"}
    user = UserCreate(**payload)
    assert user.name == "Ivan"
    assert user.email == "ivan@example.com"


def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(name="Ivan", email="not-an-email", password="123")


def test_user_response_from_attributes():
    class MockUser:
        id = 10
        name = "Admin"
        email = "admin@test.com"
        is_admin = True

    user_res = UserResponse.model_validate(MockUser())
    assert user_res.id == 10
    assert user_res.is_admin is True