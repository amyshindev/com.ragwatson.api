"""ML 데이터 인입 컨트롤러."""

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from ml_data.schemas.audio_features import AudioFeatureCreate, AudioFeatureRead
from ml_data.schemas.generation_logs import GenerationLogCreate, GenerationLogRead
from ml_data.schemas.user_events import UserEventCreate, UserEventRead
from ml_data.schemas.visual_ratings import VisualRatingCreate, VisualRatingRead
from ml_data.service.ml_data_service import MlDataService

logger = logging.getLogger(__name__)


class MlDataController:
    def __init__(self, svc: MlDataService) -> None:
        self._svc = svc

    async def create_audio_feature(
        self, session: AsyncSession, body: AudioFeatureCreate
    ) -> AudioFeatureRead:
        result = await self._svc.ingest_audio_feature(session, body)
        logger.info("[MlDataController] audio_feature id=%s", result.id)
        return result

    async def create_user_event(
        self, session: AsyncSession, body: UserEventCreate
    ) -> UserEventRead:
        result = await self._svc.log_user_event(session, body)
        logger.info("[MlDataController] user_event id=%s", result.id)
        return result

    async def create_generation_log(
        self, session: AsyncSession, body: GenerationLogCreate
    ) -> GenerationLogRead:
        result = await self._svc.log_generation(session, body)
        logger.info("[MlDataController] generation_log id=%s", result.id)
        return result

    async def create_visual_rating(
        self, session: AsyncSession, body: VisualRatingCreate
    ) -> VisualRatingRead:
        result = await self._svc.submit_rating(session, body)
        logger.info("[MlDataController] visual_rating id=%s", result.id)
        return result
