from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import get_database_url, is_database_configured

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def _ensure_engine() -> None:
    global _engine, _session_factory, engine, AsyncSessionLocal
    if _engine is not None:
        return
    _engine = create_async_engine(get_database_url(), pool_pre_ping=True)
    _session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    engine = _engine
    AsyncSessionLocal = _session_factory


async def dispose_engine() -> None:
    global _engine, _session_factory, engine, AsyncSessionLocal
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _session_factory = None
    engine = None
    AsyncSessionLocal = None


# Back-compat: None until first DB use (chat does not need DB).
engine: AsyncEngine | None = None
AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if not is_database_configured():
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL is not set.",
        )
    _ensure_engine()
    assert _session_factory is not None
    async with _session_factory() as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_db)]
