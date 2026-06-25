from __future__ import annotations

import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from audio.adapter.inbound.api.schemas.audio_features import (
    AudioFeatureCreate,
    AudioFeatureRead,
    AudioFeatureStatusRead,
)
from audio.app._transaction import run_committed
from audio.app.ports.input.audio_feature_use_case import AudioFeatureUseCase
from audio.app.ports.output.audio_feature_repository import AudioFeatureRepository

log = logging.getLogger(__name__)


class AudioFeatureInteractor(AudioFeatureUseCase):
    def __init__(
        self,
        session: AsyncSession,
        repository: AudioFeatureRepository,
    ) -> None:
        self._session = session
        self._repository = repository

    async def ingest(self, body: AudioFeatureCreate) -> AudioFeatureRead:
        row = await run_committed(self._session, lambda: self._repository.create(body))
        log.info("[AudioFeatureInteractor] ingest id=%s", row.id)
        return AudioFeatureRead.model_validate(row)

    async def get(self, feature_id: UUID) -> AudioFeatureRead:
        row = await self._repository.get(feature_id)
        if row is None:
            raise HTTPException(status_code=404, detail="AudioFeature not found")
        return AudioFeatureRead.model_validate(row)

    async def get_status(self, feature_id: UUID) -> AudioFeatureStatusRead:
        row = await self._repository.get(feature_id)
        if row is None:
            raise HTTPException(status_code=404, detail="AudioFeature not found")
        return AudioFeatureStatusRead.model_validate(row)

    async def list_by_user(self, user_id: int, limit: int, offset: int) -> list[AudioFeatureRead]:
        rows = await self._repository.list_by_user(user_id, limit, offset)
        return [AudioFeatureRead.model_validate(r) for r in rows]

    async def update_inference_result(self, feature_id: UUID, result: dict) -> AudioFeatureRead:
        if await self._repository.get(feature_id) is None:
            raise HTTPException(status_code=404, detail="AudioFeature not found")
        row = await run_committed(
            self._session,
            lambda: self._repository.update_inference_result(feature_id, result),
        )
        return AudioFeatureRead.model_validate(row)

    async def update_visual_mapping(self, feature_id: UUID, mapping: dict) -> AudioFeatureRead:
        if await self._repository.get(feature_id) is None:
            raise HTTPException(status_code=404, detail="AudioFeature not found")
        row = await run_committed(
            self._session,
            lambda: self._repository.update_visual_mapping(feature_id, mapping),
        )
        return AudioFeatureRead.model_validate(row)

    async def update_beat_analysis(self, feature_id: UUID, analysis: dict) -> AudioFeatureRead:
        if await self._repository.get(feature_id) is None:
            raise HTTPException(status_code=404, detail="AudioFeature not found")
        row = await run_committed(
            self._session,
            lambda: self._repository.update_beat_analysis(feature_id, analysis),
        )
        return AudioFeatureRead.model_validate(row)
