import pytest
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/test_db"
ASYNC_SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
AsyncTestingSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
async def async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncTestingSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
async def client(async_db) -> AsyncClient:
    async def override_get_db():
        yield async_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()