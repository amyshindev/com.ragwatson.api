from uuid import UUID

from fastapi import APIRouter, Depends, Query

from audio.adapter.inbound.api.schemas.generation_logs import (
    GenerationLogCreate,
    GenerationLogRead,
    GenerationLogStatusRead,
)
from audio.app.ports.input.generation_log_use_case import GenerationLogUseCase
from audio.dependencies.generation_log import get_generation_log_use_case

generation_logs_router = APIRouter(prefix="/api/ml", tags=["ml-data"])


@generation_logs_router.post("/generations", response_model=GenerationLogRead)
async def post_generation_log(
    body: GenerationLogCreate,
    use_case: GenerationLogUseCase = Depends(get_generation_log_use_case),
) -> GenerationLogRead:
    """Layer 3: AI 생성 로그 (status=pending)."""
    return await use_case.log_generation(body)


@generation_logs_router.get(
    "/generations/{generation_id}/status",
    response_model=GenerationLogStatusRead,
)
async def get_generation_log_status(
    generation_id: UUID,
    use_case: GenerationLogUseCase = Depends(get_generation_log_use_case),
) -> GenerationLogStatusRead:
    return await use_case.get_status(generation_id)


@generation_logs_router.get(
    "/generations/{generation_id}",
    response_model=GenerationLogRead,
)
async def get_generation_log(
    generation_id: UUID,
    use_case: GenerationLogUseCase = Depends(get_generation_log_use_case),
) -> GenerationLogRead:
    return await use_case.get(generation_id)


@generation_logs_router.get("/generations", response_model=list[GenerationLogRead])
async def list_generation_logs(
    user_id: int = Query(..., ge=1),
    status: str | None = None,
    limit: int = Query(default=20, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_case: GenerationLogUseCase = Depends(get_generation_log_use_case),
) -> list[GenerationLogRead]:
    return await use_case.list_by_user(user_id, status, limit, offset)
