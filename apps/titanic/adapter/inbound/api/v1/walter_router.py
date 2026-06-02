import logging

from fastapi import APIRouter

from db.session import DbSession
from titanic.app.use_cases.walter_interactor import WalterInteractor

log = logging.getLogger(__name__)

walter_router = APIRouter(prefix="/api/walter/v1", tags=["walter-reader"])


@walter_router.get("/preview")
async def read_preview_data(session: DbSession) -> dict:
    log.info("[WalterRouter] preview 조회 시작")
    use_case = WalterInteractor(session)
    result = await use_case.get_preview_records([])
    log.info("[WalterRouter] preview 조회 완료 — rows=%s", result["count"])
    return result
