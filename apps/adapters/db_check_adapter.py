"""Adapter: AsyncSession → simple JSON-serializable DB health payload."""

from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DbCheckAdapter:
    """Wraps a trivial Neon/Postgres round-trip so routes stay thin."""

    async def check_now(self, session: AsyncSession) -> dict[str, Any]:
        try:
            result = await session.execute(text("SELECT NOW()"))
            now = result.scalar()
            return {"status": "success", "neon_time": now}
        except Exception as e:
            return {"status": "error", "message": str(e)}


db_check_adapter = DbCheckAdapter()
