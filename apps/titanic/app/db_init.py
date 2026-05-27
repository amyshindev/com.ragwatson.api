import logging

from sqlalchemy import select

import database
from core.config import is_database_configured
from titanic.app.models.passenger import Passenger

log = logging.getLogger(__name__)


async def init_titanic_tables() -> None:
    if not is_database_configured():
        log.info("Titanic DB initialization skipped (DATABASE_URL not set)")
        return

    from orm_registry import import_all_models

    import_all_models()

    await database.init_db()
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
