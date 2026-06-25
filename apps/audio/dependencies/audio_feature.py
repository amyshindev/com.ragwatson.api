from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from audio.adapter.outbound.pg.audio_feature_pg_repository import AudioFeaturePgRepository
from audio.app.ports.input.audio_feature_use_case import AudioFeatureUseCase
from audio.app.ports.output.audio_feature_repository import AudioFeatureRepository
from audio.app.use_cases.audio_feature_interactor import AudioFeatureInteractor
from core.matrix.oracle_database import get_db


def get_audio_feature_use_case(
    db: AsyncSession = Depends(get_db),
) -> AudioFeatureUseCase:
    repository: AudioFeatureRepository = AudioFeaturePgRepository(session=db)
    return AudioFeatureInteractor(session=db, repository=repository)
