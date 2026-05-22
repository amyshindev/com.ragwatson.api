import logging

from sqlalchemy.ext.asyncio import AsyncSession

from ml_data.models.user_events import UserEvent
from ml_data.schemas.user_events import UserEventCreate

logger = logging.getLogger(__name__)


class UserEventRepository:
    async def create(self, session: AsyncSession, body: UserEventCreate) -> UserEvent:
        data = body.model_dump()
        user_id = data.pop("user_id")
        row = UserEvent(user_id=user_id, **data)
        session.add(row)
        await session.flush()
        await session.refresh(row)
        logger.info(
            "[UserEventRepository] create id=%s type=%s",
            row.id,
            row.event_type,
        )
        return row
