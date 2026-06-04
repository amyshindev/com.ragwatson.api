"""Neon PostgreSQL 비동기 연결 (SQLAlchemy 2.0)."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from core.config import get_database_url, is_database_configured

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None

engine: AsyncEngine | None = None
AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None


class Base(DeclarativeBase):
    pass


def _ensure_engine() -> None:
    global _engine, _session_factory, engine, AsyncSessionLocal
    if _engine is not None:
        return
    _engine = create_async_engine(
        get_database_url(),
        echo=False,
        pool_pre_ping=True,
    )
    _session_factory = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    engine = _engine
    AsyncSessionLocal = _session_factory


async def init_db() -> None:
    """ORM 메타데이터로 테이블 생성 (Neon PostgreSQL)."""
    if not is_database_configured():
        return
    _ensure_engine()
    assert engine is not None
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def dispose_engine() -> None:
    global _engine, _session_factory, engine, AsyncSessionLocal
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _session_factory = None
    engine = None
    AsyncSessionLocal = None


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

__all__ = [
    "AsyncSessionLocal",
    "Base",
    "DbSession",
    "dispose_engine",
    "engine",
    "get_db",
    "init_db",
]
