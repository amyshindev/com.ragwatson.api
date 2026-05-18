from core.config import is_database_configured
from database import Base
from db.session import _ensure_engine


async def init_secom_tables() -> None:
    if not is_database_configured():
        raise RuntimeError("DATABASE_URL is not set")

    from secom.app.models.user import User  # noqa: F401 — register metadata

    _ensure_engine()
    from db.session import engine

    assert engine is not None
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
