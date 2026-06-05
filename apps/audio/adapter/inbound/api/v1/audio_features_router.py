from uuid import UUID

from fastapi import APIRouter, Depends, Query

from ml_data.adapter.inbound.api.schemas.audio_features import (
    AudioFeatureCreate,
    AudioFeatureRead,
    AudioFeatureStatusRead,
)
from ml_data.app.ports.input.audio_feature_use_case import AudioFeatureUseCase
from ml_data.dependencies.audio_feature import get_audio_feature_use_case

audio_features_router = APIRouter(prefix="/api/ml", tags=["ml-data"])


@audio_features_router.post("/audio-features", response_model=AudioFeatureRead)
async def post_audio_feature(
    body: AudioFeatureCreate,
    use_case: AudioFeatureUseCase = Depends(get_audio_feature_use_case),
) -> AudioFeatureRead:
    """Layer 1: 음악 분석 피처 인입 (processing_status=pending)."""
    return await use_case.ingest(body)


@audio_features_router.get(
    "/audio-features/{feature_id}/status",
    response_model=AudioFeatureStatusRead,
)
async def get_audio_feature_status(
    feature_id: UUID,
    use_case: AudioFeatureUseCase = Depends(get_audio_feature_use_case),
) -> AudioFeatureStatusRead:
    return await use_case.get_status(feature_id)


@audio_features_router.get(
    "/audio-features/{feature_id}",
    response_model=AudioFeatureRead,
)
async def get_audio_feature(
    feature_id: UUID,
    use_case: AudioFeatureUseCase = Depends(get_audio_feature_use_case),
) -> AudioFeatureRead:
    return await use_case.get(feature_id)


@audio_features_router.get("/audio-features", response_model=list[AudioFeatureRead])
async def list_audio_features(
    user_id: int = Query(..., ge=1),
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_case: AudioFeatureUseCase = Depends(get_audio_feature_use_case),
) -> list[AudioFeatureRead]:
    return await use_case.list_by_user(user_id, limit, offset)
