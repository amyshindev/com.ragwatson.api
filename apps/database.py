"""Neon PostgreSQL — ``core.matrix.oracle_database`` 단일 소스 (가변 export는 __getattr__)."""

from core.matrix import oracle_database as _oracle

Base = _oracle.Base
DbSession = _oracle.DbSession
_ensure_engine = _oracle._ensure_engine
dispose_engine = _oracle.dispose_engine
get_db = _oracle.get_db
init_db = _oracle.init_db

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
        return getattr(_oracle, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
