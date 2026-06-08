"""Neon PostgreSQL — ``core.database.database_manager`` 단일 소스 (가변 export는 __getattr__)."""

from core.database import database_manager as _database


Base = _database.Base
DbSession = _database.DbSession
_ensure_engine = _database._ensure_engine
dispose_engine = _database.dispose_engine
get_db = _database.get_db
init_db = _database.init_db

__all__ = [
    "AsyncSessionLocal",
    "Base",
    "DbSession",
    "_ensure_engine",
    "dispose_engine",
    "engine",
    "get_db",
    "init_db",
]

# engine / AsyncSessionLocal 은 _ensure_engine() 이후에만 설정되므로
# import 시점 복사(from ... import engine)를 쓰면 항상 None 이 남는다.


def __getattr__(name: str):
    if name in ("engine", "AsyncSessionLocal"):
        return getattr(_database, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
