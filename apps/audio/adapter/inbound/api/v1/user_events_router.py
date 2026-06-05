from fastapi import APIRouter, Depends, Query

from ml_data.adapter.inbound.api.schemas.user_events import UserEventCreate, UserEventRead
from ml_data.app.ports.input.user_event_use_case import UserEventUseCase
from ml_data.dependencies.user_event import get_user_event_use_case

user_events_router = APIRouter(prefix="/api/ml", tags=["ml-data"])


@user_events_router.post("/events", response_model=UserEventRead)
async def post_user_event(
    body: UserEventCreate,
    use_case: UserEventUseCase = Depends(get_user_event_use_case),
) -> UserEventRead:
    """Layer 2: 사용자 행동 이벤트."""
    return await use_case.log_event(body)


@user_events_router.get("/events", response_model=list[UserEventRead])
async def list_user_events(
    user_id: int = Query(..., ge=1),
    event_type: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    use_case: UserEventUseCase = Depends(get_user_event_use_case),
) -> list[UserEventRead]:
    return await use_case.list_by_user(user_id, event_type, limit)
