import logging

from sqlalchemy import text

from core.config import is_database_configured
import database

log = logging.getLogger(__name__)

_USERS_COLUMN_PATCHES: tuple[str, ...] = (
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS nickname VARCHAR(64)",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255)",
)


async def init_friday13th_tables() -> None:
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
        await conn.execute(
            text(
                "UPDATE users SET nickname = username "
                "WHERE nickname IS NULL AND username IS NOT NULL"
            )
        )
        await conn.execute(
            text(
                """
                DO $$
                BEGIN
                  IF EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_schema = current_schema()
                      AND table_name = 'users'
                      AND column_name = 'password'
                  ) THEN
                    UPDATE users SET password_hash = password
                    WHERE password_hash IS NULL AND password IS NOT NULL;
                  END IF;
                END $$;
                """
            )
        )
        from domain_intake.db_init import (
            drop_membership_inquiries_table,
            migrate_legacy_domain_intake_records,
        )

        await drop_membership_inquiries_table(conn)
        await migrate_legacy_domain_intake_records(conn)
    log.info("friday13th users table ready (create_all + column patches)")


async def init_secom_tables() -> None:
    """Backward-compatible alias."""
    await init_friday13th_tables()
