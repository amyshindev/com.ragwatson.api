import logging



from sqlalchemy import text



import database

from core.config import is_database_configured



log = logging.getLogger(__name__)





async def init_automata_tables() -> None:

    if not is_database_configured():

        log.info("Automata DB initialization skipped (DATABASE_URL not set)")

        return



    from orm_registry import import_all_models



    import_all_models()

    database._ensure_engine()

    assert database.engine is not None



    async with database.engine.begin() as conn:

        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

        await conn.run_sync(database.Base.metadata.create_all)



    log.info("Automata tables ready (pgvector extension ensured)")


