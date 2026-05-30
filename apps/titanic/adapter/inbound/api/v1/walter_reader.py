import logging

from fastapi import APIRouter

from db.session import DbSession
from titanic.adapter.inbound.api.v1.james_router import get_last_uploaded_passenger_ids
from titanic.app.use_cases.walter_query import WalterQueryUseCase

log = logging.getLogger(__name__)

walter_router = APIRouter(prefix="/api/walter/v1", tags=["walter-reader"])


@walter_router.get("/preview")
async def read_preview_data(session: DbSession) -> dict:
    log.info("[WalterRouter] preview 조회 시작")
    last_uploaded_ids = get_last_uploaded_passenger_ids()
    if not last_uploaded_ids:
        log.info("[WalterRouter] preview 조회 중단 — 최근 업로드 기록 없음")
        return {"count": 0, "items": []}

    use_case = WalterQueryUseCase(session)
    result = await use_case.get_preview_records(last_uploaded_ids)
    log.info("[WalterRouter] preview 조회 완료 — rows=%s", result["count"])
    return result
