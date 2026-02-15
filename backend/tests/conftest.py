import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import Base, get_db
from app.config import settings

# Используем асинхронный URL. 
# Если в settings.database_url уже есть +asyncpg, используем его, 
# иначе принудительно меняем протокол для тестов.
TEST_DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

# Создаем единственный асинхронный движок для тестов
async_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
)

# Фабрика асинхронных сессий
AsyncTestingSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

@pytest.fixture(scope="session")
def event_loop():
    """Создает экземпляр event loop для всей тестовой сессии."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function", autouse=True)
async def setup_db():
    """
    Автоматически создает и удаляет таблицы перед/после каждого теста.
    Использует run_sync для выполнения синхронных команд DDL.
    """
    async with async_engine.begin() as conn:
        # Очищаем базу перед тестом (важно для изоляции)
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def async_db() -> AsyncGenerator[AsyncSession, None]:
    """Фикстура для получения сессии БД в тестах."""
    async with AsyncTestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="function")
async def client(async_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Асинхронный клиент для тестирования эндпоинтов FastAPI."""
    
    # Переопределяем зависимость get_db, чтобы приложение использовало тестовую сессию
    async def override_get_db():
        yield async_db

    app.dependency_overrides[get_db] = override_get_db

    # В новых версиях HTTPX используется ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    # Очищаем переопределения после теста
    app.dependency_overrides.clear()