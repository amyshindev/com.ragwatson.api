from uuid import UUID

from fastapi import APIRouter, Depends, Query

from audio.adapter.inbound.api.schemas.visual_ratings import (
    AbTestResultRead,
    VisualRatingAvgRead,
    VisualRatingCreate,
    VisualRatingPlatformAvgRead,
    VisualRatingRead,
)
from audio.app.ports.input.visual_rating_use_case import VisualRatingUseCase
from audio.dependencies.visual_rating import get_visual_rating_use_case

visual_ratings_router = APIRouter(prefix="/api/ml", tags=["ml-data"])


@visual_ratings_router.post("/ratings", response_model=VisualRatingRead)
async def post_visual_rating(
    body: VisualRatingCreate,
    use_case: VisualRatingUseCase = Depends(get_visual_rating_use_case),
) -> VisualRatingRead:
    """Layer 4: 비주얼 평가·레이블."""
    return await use_case.submit_rating(body)


@visual_ratings_router.get("/ratings/avg", response_model=VisualRatingAvgRead)
async def get_avg_scores(
    generation_id: UUID = Query(...),
    use_case: VisualRatingUseCase = Depends(get_visual_rating_use_case),
) -> VisualRatingAvgRead:
    return await use_case.get_avg_scores(generation_id)


@visual_ratings_router.get(
    "/ratings/platform-avg",
    response_model=VisualRatingPlatformAvgRead,
)
async def get_platform_avg(
    generation_id: UUID = Query(...),
    platform: str | None = None,
    use_case: VisualRatingUseCase = Depends(get_visual_rating_use_case),
) -> VisualRatingPlatformAvgRead:
    return await use_case.get_platform_avg(generation_id, platform)


@visual_ratings_router.get(
    "/ratings/ab-test/{ab_test_id}",
    response_model=AbTestResultRead,
)
async def get_ab_test_result(
    ab_test_id: str,
    use_case: VisualRatingUseCase = Depends(get_visual_rating_use_case),
) -> AbTestResultRead:
    return await use_case.get_ab_test_result(ab_test_id)


@visual_ratings_router.get("/ratings", response_model=list[VisualRatingRead])
async def list_ratings(
    generation_id: UUID = Query(...),
    use_case: VisualRatingUseCase = Depends(get_visual_rating_use_case),
) -> list[VisualRatingRead]:
    return await use_case.get_ratings_by_generation(generation_id)
