import pytest
from app.repositories.user_repo import UserRepository
from pydantic import BaseModel


# Мокаем схему, чтобы тест не зависел от файла schemas/user.py
class MockUserCreate(BaseModel):
    name: str
    email: str
    password: str


@pytest.mark.asyncio
async def test_create_user(async_db):
    repo = UserRepository(async_db)
    user_data = MockUserCreate(name="Async User", email="async@test.com", password="123")

    user = await repo.create(user_data, hashed_password="hashed_123")

    assert user.id is not None
    assert user.email == "async@test.com"
    assert user.hashed_password == "hashed_123"


@pytest.mark.asyncio
async def test_get_user_by_email(async_db):
    repo = UserRepository(async_db)
    user_data = MockUserCreate(name="Find Me", email="find@test.com", password="123")
    await repo.create(user_data, hashed_password="pw")

    found_user = await repo.get_by_email("find@test.com")
    assert found_user is not None
    assert found_user.name == "Find Me"


@pytest.mark.asyncio
async def test_get_user_by_id(async_db):
    repo = UserRepository(async_db)
    user_data = MockUserCreate(name="ID User", email="id@test.com", password="123")
    created = await repo.create(user_data, hashed_password="pw")

    found = await repo.get_by_id(created.id)
    assert found is not None
    assert found.id == created.id