import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from audio.adapter.inbound.api.schemas.audio_features import AudioFeatureCreate
from audio.adapter.outbound.orm.audio_feature_orm import AudioFeature
from audio.app.ports.output.audio_feature_repository import AudioFeatureRepository

logger = logging.getLogger(__name__)

_INFERENCE_FIELDS = {
    "predicted_visual_style",
    "predicted_color_palette",
    "visual_embedding",
    "model_version",
    "processing_status",
    "error_message",
}
_VISUAL_MAPPING_FIELDS = {
    "visual_motion_intensity",
    "visual_texture_type",
    "visual_color_temperature",
    "visual_rhythm_sync",
    "genre_to_visual_mapping",
    "mood_to_color_mapping",
}
_BEAT_FIELDS = {
    "beat_timestamps",
    "highlight_start_sec",
    "highlight_end_sec",
    "onset_strength",
}


class AudioFeaturePgRepository(AudioFeatureRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, body: AudioFeatureCreate) -> AudioFeature:
        data = body.model_dump()
        user_id = data.pop("user_id")
        row = AudioFeature(user_id=user_id, processing_status="pending", **data)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        logger.info("[AudioFeaturePgRepository] create id=%s user_id=%s", row.id, user_id)
        return row

    async def get(self, feature_id: UUID) -> AudioFeature | None:
        result = await self._session.execute(
            select(AudioFeature).where(AudioFeature.id == feature_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> list[AudioFeature]:
        result = await self._session.execute(
            select(AudioFeature)
            .where(AudioFeature.user_id == user_id)
            .order_by(AudioFeature.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def _update_fields(
        self, feature_id: UUID, payload: dict, allowed: set[str]
    ) -> AudioFeature:
        row = await self.get(feature_id)
        if row is None:
            raise ValueError(f"AudioFeature not found: {feature_id}")
        for key, value in payload.items():
            if key in allowed:
                setattr(row, key, value)
        await self._session.flush()
        await self._session.refresh(row)
        return row

    async def update_inference_result(
        self, feature_id: UUID, result: dict
    ) -> AudioFeature:
        payload = dict(result)
        if payload.get("processing_status") == "done":
            payload.setdefault("inferred_at", datetime.now(timezone.utc))
        return await self._update_fields(feature_id, payload, _INFERENCE_FIELDS)

    async def update_visual_mapping(
        self, feature_id: UUID, mapping: dict
    ) -> AudioFeature:
        return await self._update_fields(feature_id, mapping, _VISUAL_MAPPING_FIELDS)

    async def update_beat_analysis(
        self, feature_id: UUID, analysis: dict
    ) -> AudioFeature:
        return await self._update_fields(feature_id, analysis, _BEAT_FIELDS)
