from fastapi import APIRouter

from ml_data.adapter.inbound.api.v1.audio_features_router import audio_features_router
from ml_data.adapter.inbound.api.v1.generation_logs_router import generation_logs_router
from ml_data.adapter.inbound.api.v1.training_export_router import training_export_router
from ml_data.adapter.inbound.api.v1.user_events_router import user_events_router
from ml_data.adapter.inbound.api.v1.visual_ratings_router import visual_ratings_router

ml_data_router = APIRouter()
ml_data_router.include_router(audio_features_router)
ml_data_router.include_router(user_events_router)
ml_data_router.include_router(generation_logs_router)
ml_data_router.include_router(visual_ratings_router)
ml_data_router.include_router(training_export_router)

__all__ = ["ml_data_router"]
