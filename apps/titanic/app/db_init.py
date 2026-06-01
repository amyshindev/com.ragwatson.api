import logging

from sqlalchemy import select

import database
from core.config import is_database_configured
from titanic.adapter.outbound.orm.titanic_model import Passenger

log = logging.getLogger(__name__)


async def ensure_titanic_schema() -> None:
    """passengers 테이블 등 ORM 스키마가 DB에 존재하도록 보장."""
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
            # Check if Passenger table already has data
            result = await session.execute(select(Passenger).limit(1))
            passenger = result.scalar_one_or_none()
            if passenger is None:
                log.info("Titanic passengers table is empty. Internal file seeding skipped.")
            else:
                log.info("Titanic passengers table already contains data. Seeding skipped.")
