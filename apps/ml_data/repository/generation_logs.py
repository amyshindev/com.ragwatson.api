import logging

from sqlalchemy.ext.asyncio import AsyncSession

from ml_data.models.generation_logs import GenerationLog
from ml_data.schemas.generation_logs import GenerationLogCreate

logger = logging.getLogger(__name__)


class GenerationLogRepository:
    async def create(
        self, session: AsyncSession, body: GenerationLogCreate
    ) -> GenerationLog:
        data = body.model_dump()
        user_id = data.pop("user_id")
        row = GenerationLog(user_id=user_id, **data)
        session.add(row)
        await session.flush()
        await session.refresh(row)
        logger.info("[GenerationLogRepository] create id=%s status=%s", row.id, row.status)
        return row
