import pytest
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport  # Добавили ASGITransport

from app.main import app
from app.database import Base, get_db

# Используем NullPool, чтобы pytest не держал открытые соединения между тестами
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/test_db"
ASYNC_SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/test_db"

# Синхронный движок
engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Асинхронный движок
async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
AsyncTestingSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# 1. Исправляем управление Event Loop
@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# 2. Чистим БД
@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# 3. Синхронная сессия (для старых тестов)
@pytest.fixture(scope="function")
def db() -> Generator:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# 4. Асинхронная сессия (для репозиториев)
@pytest.fixture(scope="function")
async def async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncTestingSessionLocal() as session:
        yield session
        # Важно: закрытие произойдет автоматически при выходе из context manager


# 5. Исправленный AsyncClient
@pytest.fixture(scope="function")
async def client(async_db) -> AsyncClient:
    # Переопределяем зависимость в FastAPI
    async def override_get_db():
        yield async_db

    app.dependency_overrides[get_db] = override_get_db

    # НОВЫЙ СИНТАКСИС httpx 0.27+
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()