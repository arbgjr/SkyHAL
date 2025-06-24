"""Shared fixtures for pytest."""
from typing import Any, AsyncGenerator

import pytest
from _pytest.config import Config
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine


def pytest_configure(config: Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "asyncio: mark test as async")


@pytest.fixture
async def app() -> Any:
    """Fixture que retorna a aplicação FastAPI."""
    from src.presentation.api.app import app

    return app


@pytest.fixture
def test_db_url() -> str:
    """Fixture que retorna a URL do banco de dados de teste."""
    return "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def db_engine(test_db_url: str) -> AsyncGenerator[AsyncEngine, None]:
    """Fixture que retorna um engine de banco de dados para teste."""
    engine = create_async_engine(test_db_url, echo=True)
    yield engine
    await engine.dispose()


@pytest.fixture
def session_factory(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Fixture que retorna uma factory de sessão do banco de dados."""
    from src.infrastructure.database.base import Base

    Base.metadata.create_all(db_engine)
    yield AsyncSession(db_engine)
    Base.metadata.drop_all(db_engine)


@pytest.fixture(scope="function")
async def db_session(
    session_factory: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    """Create database session."""
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest.fixture(scope="function")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create test client."""
    from httpx import ASGITransport

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
