import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from audio.adapter.inbound.api.schemas.user_events import UserEventCreate
from audio.adapter.outbound.orm.user_event_orm import UserEvent
from audio.app.ports.output.user_event_repository import UserEventRepository

logger = logging.getLogger(__name__)


class UserEventPgRepository(UserEventRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, body: UserEventCreate) -> UserEvent:
        data = body.model_dump()
        user_id = data.pop("user_id")
        row = UserEvent(user_id=user_id, **data)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        logger.info(
            "[UserEventPgRepository] create id=%s type=%s",
            row.id,
            row.event_type,
        )
        return row

    async def list_by_user(
        self,
        user_id: int,
        event_type: str | None = None,
        limit: int = 50,
    ) -> list[UserEvent]:
        stmt = (
            select(UserEvent)
            .where(UserEvent.user_id == user_id)
            .order_by(UserEvent.created_at.desc())
            .limit(limit)
        )
        if event_type:
            stmt = stmt.where(UserEvent.event_type == event_type)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
