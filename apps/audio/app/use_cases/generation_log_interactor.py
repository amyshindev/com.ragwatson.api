from __future__ import annotations

import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from audio.adapter.inbound.api.schemas.generation_logs import (
    GenerationLogCreate,
    GenerationLogRead,
    GenerationLogStatusRead,
)
from audio.app._transaction import run_committed
from audio.app.ports.input.generation_log_use_case import GenerationLogUseCase
from audio.app.ports.output.generation_log_repository import GenerationLogRepository

log = logging.getLogger(__name__)


class GenerationLogInteractor(GenerationLogUseCase):
    def __init__(
        self,
        session: AsyncSession,
        repository: GenerationLogRepository,
    ) -> None:
        self._session = session
        self._repository = repository

    async def log_generation(self, body: GenerationLogCreate) -> GenerationLogRead:
        row = await run_committed(
            self._session, lambda: self._repository.create(body)
        )
        log.info("[GenerationLogInteractor] log_generation id=%s", row.id)
        return GenerationLogRead.model_validate(row)

    async def get(self, generation_id: UUID) -> GenerationLogRead:
        row = await self._repository.get(generation_id)
        if row is None:
            raise HTTPException(status_code=404, detail="GenerationLog not found")
        return GenerationLogRead.model_validate(row)

    async def get_status(self, generation_id: UUID) -> GenerationLogStatusRead:
        row = await self._repository.get(generation_id)
        if row is None:
            raise HTTPException(status_code=404, detail="GenerationLog not found")
        return GenerationLogStatusRead.model_validate(row)

    async def list_by_user(
        self,
        user_id: int,
        status: str | None,
        limit: int,
        offset: int,
    ) -> list[GenerationLogRead]:
        rows = await self._repository.list_by_user(user_id, status, limit, offset)
        return [GenerationLogRead.model_validate(r) for r in rows]

    async def update_result(
        self, generation_id: UUID, result: dict
    ) -> GenerationLogRead:
        if await self._repository.get(generation_id) is None:
            raise HTTPException(status_code=404, detail="GenerationLog not found")
        row = await run_committed(
            self._session,
            lambda: self._repository.update_result(generation_id, result),
        )
        return GenerationLogRead.model_validate(row)

    async def update_loop_meta(
        self, generation_id: UUID, meta: dict
    ) -> GenerationLogRead:
        if await self._repository.get(generation_id) is None:
            raise HTTPException(status_code=404, detail="GenerationLog not found")
        row = await run_committed(
            self._session,
            lambda: self._repository.update_loop_meta(generation_id, meta),
        )
        return GenerationLogRead.model_validate(row)
