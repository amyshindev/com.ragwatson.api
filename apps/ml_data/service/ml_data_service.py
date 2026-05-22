"""ML 4-Layer 인입 비즈니스 로직."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from ml_data.repository import MlDataRepositories
from ml_data.schemas.audio_features import AudioFeatureCreate, AudioFeatureRead
from ml_data.schemas.generation_logs import GenerationLogCreate, GenerationLogRead
from ml_data.schemas.user_events import UserEventCreate, UserEventRead
from ml_data.schemas.visual_ratings import VisualRatingCreate, VisualRatingRead

logger = logging.getLogger(__name__)


class MlDataService:
    def __init__(self, repos: MlDataRepositories) -> None:
        self._repos = repos

    async def ingest_audio_feature(
        self, session: AsyncSession, body: AudioFeatureCreate
    ) -> AudioFeatureRead:
        row = await self._repos.audio_features.create(session, body)
        return AudioFeatureRead.model_validate(row)

    async def log_user_event(
        self, session: AsyncSession, body: UserEventCreate
    ) -> UserEventRead:
        row = await self._repos.user_events.create(session, body)
        return UserEventRead.model_validate(row)

    async def log_generation(
        self, session: AsyncSession, body: GenerationLogCreate
    ) -> GenerationLogRead:
        row = await self._repos.generation_logs.create(session, body)
        return GenerationLogRead.model_validate(row)

    async def submit_rating(
        self, session: AsyncSession, body: VisualRatingCreate
    ) -> VisualRatingRead:
        row = await self._repos.visual_ratings.create(session, body)
        return VisualRatingRead.model_validate(row)
