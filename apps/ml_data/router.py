"""POST /api/ml/* — 4-Layer ML 데이터 수집."""

import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import DbSession
from ml_data.controller import MlDataController
from ml_data.repository import MlDataRepositories
from ml_data.schemas.audio_features import AudioFeatureCreate, AudioFeatureRead
from ml_data.schemas.generation_logs import GenerationLogCreate, GenerationLogRead
from ml_data.schemas.user_events import UserEventCreate, UserEventRead
from ml_data.schemas.visual_ratings import VisualRatingCreate, VisualRatingRead
from ml_data.service.ml_data_service import MlDataService

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ml", tags=["ml-data"])

_repos = MlDataRepositories()
_svc = MlDataService(_repos)
_ctrl = MlDataController(_svc)

T = TypeVar("T", bound=BaseModel)


async def _with_commit(
    session: AsyncSession,
    work: Callable[[], Awaitable[T]],
) -> T:
    try:
        result = await work()
        await session.commit()
        return result
    except HTTPException:
        await session.rollback()
        raise
    except Exception as exc:
        await session.rollback()
        log.exception("ml_data transaction failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/audio-features", response_model=AudioFeatureRead)
async def post_audio_feature(
    body: AudioFeatureCreate,
    session: DbSession,
) -> AudioFeatureRead:
    """Layer 1: 음악 분석 피처 인입."""
    return await _with_commit(
        session, lambda: _ctrl.create_audio_feature(session, body)
    )


@router.post("/events", response_model=UserEventRead)
async def post_user_event(
    body: UserEventCreate,
    session: DbSession,
) -> UserEventRead:
    """Layer 2: 사용자 행동 이벤트."""
    return await _with_commit(session, lambda: _ctrl.create_user_event(session, body))


@router.post("/generations", response_model=GenerationLogRead)
async def post_generation_log(
    body: GenerationLogCreate,
    session: DbSession,
) -> GenerationLogRead:
    """Layer 3: AI 생성 로그."""
    return await _with_commit(
        session, lambda: _ctrl.create_generation_log(session, body)
    )


@router.post("/ratings", response_model=VisualRatingRead)
async def post_visual_rating(
    body: VisualRatingCreate,
    session: DbSession,
) -> VisualRatingRead:
    """Layer 4: 비주얼 평가·레이블."""
    return await _with_commit(
        session, lambda: _ctrl.create_visual_rating(session, body)
    )
