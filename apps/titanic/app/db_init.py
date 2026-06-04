import logging

from sqlalchemy import select

import database
from core.config import is_database_configured
from titanic.adapter.outbound.orm.person_orm import PersonOrm

log = logging.getLogger(__name__)


async def ensure_titanic_schema() -> None:
    """titanic_persons / titanic_bookings 테이블이 DB에 존재하도록 보장."""
    if not is_database_configured():
        return

    from orm_registry import import_all_models

    import_all_models()
    await database.init_db()


async def init_titanic_tables() -> None:
    if not is_database_configured():
        log.info("Titanic DB initialization skipped (DATABASE_URL not set)")
        return

    await ensure_titanic_schema()
    database._ensure_engine()
    assert database.engine is not None

    async with database.AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(PersonOrm).limit(1))
            person = result.scalar_one_or_none()
            if person is None:
                log.info("Titanic persons table is empty.")
            else:
                log.info("Titanic persons table already contains data.")
