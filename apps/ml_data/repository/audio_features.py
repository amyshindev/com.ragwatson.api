import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ml_data.models.audio_features import AudioFeature
from ml_data.schemas.audio_features import AudioFeatureCreate

logger = logging.getLogger(__name__)


class AudioFeatureRepository:
    async def create(
        self, session: AsyncSession, body: AudioFeatureCreate
    ) -> AudioFeature:
        data = body.model_dump()
        user_id = data.pop("user_id")
        row = AudioFeature(user_id=user_id, **data)
        session.add(row)
        await session.flush()
        await session.refresh(row)
        logger.info("[AudioFeatureRepository] create id=%s user_id=%s", row.id, user_id)
        return row

    async def get_by_workspace(
        self, session: AsyncSession, workspace_id: int, limit: int = 50
    ) -> list[AudioFeature]:
        result = await session.execute(
            select(AudioFeature)
            .where(AudioFeature.workspace_id == workspace_id)
            .order_by(AudioFeature.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_user(
        self, session: AsyncSession, user_id: int, limit: int = 50
    ) -> list[AudioFeature]:
        result = await session.execute(
            select(AudioFeature)
            .where(AudioFeature.user_id == user_id)
            .order_by(AudioFeature.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
