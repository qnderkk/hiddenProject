import pytest
from sqlalchemy.exc import IntegrityError
from app.models.user import User

"""
Тестирование модели User:
- Создание пользователя и проверка маппинга полей (name, email, is_admin).
- Проверка уникальности email (ожидание IntegrityError при дубликате).
- Проверка значения по умолчанию для флага администратора (False).
"""

def test_create_user(db):
    user = User(
        name="John Doe",
        email="john@example.com",
        hashed_password="hashed_secret",
        is_admin=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.email == "john@example.com"
    assert user.is_admin is True


def test_user_email_unique(db):
    user1 = User(name="User 1", email="same@example.com", hashed_password="pw1")
    db.add(user1)
    db.commit()

    user2 = User(name="User 2", email="same@example.com", hashed_password="pw2")
    db.add(user2)

    with pytest.raises(IntegrityError):
        db.commit()


def test_default_is_admin(db):
    user = User(name="Regular User", email="reg@example.com", hashed_password="pw")
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.is_admin is False