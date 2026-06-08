"""Backward-compatible re-exports. Prefer ``core.database.database_manager`` or ``database``."""

from core.database.database_manager import (
    AsyncSessionLocal,
    Base,
    DbSession,
    dispose_engine,
    engine,
    get_db,
    init_db,
)

__all__ = [
    "AsyncSessionLocal",
    "Base",
    "DbSession",
    "dispose_engine",
    "engine",
    "get_db",
    "init_db",
]
