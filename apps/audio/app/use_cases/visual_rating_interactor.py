from __future__ import annotations

import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ml_data.adapter.inbound.api.schemas.visual_ratings import (
    AbTestResultRead,
    VisualRatingAvgRead,
    VisualRatingCreate,
    VisualRatingPlatformAvgRead,
    VisualRatingRead,
)
from ml_data.app._transaction import run_committed
from ml_data.app.ports.input.visual_rating_use_case import VisualRatingUseCase
from ml_data.app.ports.output.visual_rating_repository import VisualRatingRepository

log = logging.getLogger(__name__)


class VisualRatingInteractor(VisualRatingUseCase):
    def __init__(
        self,
        session: AsyncSession,
        repository: VisualRatingRepository,
    ) -> None:
        self._session = session
        self._repository = repository

    async def submit_rating(self, body: VisualRatingCreate) -> VisualRatingRead:
        row = await run_committed(
            self._session, lambda: self._repository.create(body)
        )
        log.info("[VisualRatingInteractor] submit_rating id=%s", row.id)
        return VisualRatingRead.model_validate(row)

    async def get_ratings_by_generation(
        self, generation_id: UUID
    ) -> list[VisualRatingRead]:
        rows = await self._repository.list_by_generation(generation_id)
        return [VisualRatingRead.model_validate(r) for r in rows]

    async def get_avg_scores(self, generation_id: UUID) -> VisualRatingAvgRead:
        data = await self._repository.get_avg_scores(generation_id)
        return VisualRatingAvgRead(**data)

    async def get_ab_test_result(self, ab_test_id: str) -> AbTestResultRead:
        data = await self._repository.get_ab_test_result(ab_test_id)
        return AbTestResultRead(**data)

    async def get_platform_avg(
        self, generation_id: UUID, platform: str | None
    ) -> VisualRatingPlatformAvgRead:
        data = await self._repository.get_platform_avg(generation_id, platform)
        return VisualRatingPlatformAvgRead(**data)

    async def flag_rating(
        self, rating_id: UUID, flag: str, reason: str | None
    ) -> VisualRatingRead:
        row = await run_committed(
            self._session,
            lambda: self._repository.flag_rating(rating_id, flag, reason),
        )
        return VisualRatingRead.model_validate(row)
