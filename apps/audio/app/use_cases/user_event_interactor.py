from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from audio.adapter.inbound.api.schemas.user_events import UserEventCreate, UserEventRead
from audio.app._transaction import run_committed
from audio.app.ports.input.user_event_use_case import UserEventUseCase
from audio.app.ports.output.user_event_repository import UserEventRepository

log = logging.getLogger(__name__)


class UserEventInteractor(UserEventUseCase):
    def __init__(
        self,
        session: AsyncSession,
        repository: UserEventRepository,
    ) -> None:
        self._session = session
        self._repository = repository

    async def log_event(self, body: UserEventCreate) -> UserEventRead:
        row = await run_committed(self._session, lambda: self._repository.create(body))
        log.info("[UserEventInteractor] log_event id=%s", row.id)
        return UserEventRead.model_validate(row)

    async def list_by_user(
        self, user_id: int, event_type: str | None, limit: int
    ) -> list[UserEventRead]:
        rows = await self._repository.list_by_user(user_id, event_type, limit)
        return [UserEventRead.model_validate(r) for r in rows]
