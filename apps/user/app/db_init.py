import logging

from sqlalchemy import text

from core.config import is_database_configured
import database

log = logging.getLogger(__name__)

_USERS_COLUMN_PATCHES: tuple[str, ...] = (
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS nickname VARCHAR(64)",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255)",
)


async def init_user_tables() -> None:
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
        await _seed_dev_admin_if_empty(conn)
    log.info("user tables ready (create_all + column patches)")


async def _seed_dev_admin_if_empty(conn) -> None:
    """로컬/Docker 개발용 기본 관리자 — admins 테이블이 비어 있을 때만 생성."""
    from user.adapter.outbound.pg.password_hasher import hash_password

    existing = await conn.execute(
        text("SELECT 1 FROM admins WHERE deleted_at IS NULL LIMIT 1")
    )
    if existing.scalar_one_or_none() is not None:
        return

    email = "admin@example.com"
    username = "admin"
    password_hash = hash_password("admin1234")
    await conn.execute(
        text(
            """
            INSERT INTO admins (email, username, password_hash)
            VALUES (:email, :username, :password_hash)
            """
        ),
        {"email": email, "username": username, "password_hash": password_hash},
    )
    log.warning(
        "Dev admin seeded — email=%s password=admin1234 (change in production)",
        email,
    )


async def init_secom_tables() -> None:
    """Backward-compatible alias."""
    await init_user_tables()
