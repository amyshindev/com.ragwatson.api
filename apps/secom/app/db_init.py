import logging

from sqlalchemy import text

import database
from core.config import is_database_configured

log = logging.getLogger(__name__)

_USERS_COLUMN_PATCHES: tuple[str, ...] = (
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS nickname VARCHAR(64)",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255)",
)


async def init_secom_tables() -> None:
    if not is_database_configured():
        raise RuntimeError("DATABASE_URL is not set")

    from orm_registry import import_all_models

    import_all_models()

    await database.init_db()
    database._ensure_engine()
    assert database.engine is not None
    async with database.engine.begin() as conn:
        for stmt in _USERS_COLUMN_PATCHES:
            await conn.execute(text(stmt))
    log.info("secom users table ready (create_all + column patches)")

