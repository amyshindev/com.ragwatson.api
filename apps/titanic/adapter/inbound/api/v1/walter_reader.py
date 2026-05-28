import logging

from fastapi import APIRouter

from db.session import DbSession
from titanic.adapter.inbound.api.v1.james_router import get_last_uploaded_passenger_ids
from titanic.app.ports.input.walter_use_case import WalterUseCase

log = logging.getLogger(__name__)

walter_router = APIRouter(prefix="/api/walter/v1", tags=["walter-reader"])
_walter_use_case = WalterUseCase()


@walter_router.get("/preview")
async def read_preview_data(session: DbSession) -> dict:
    log.info("[WalterRouter] preview 조회 시작")
    last_uploaded_ids = get_last_uploaded_passenger_ids()
    if not last_uploaded_ids:
        log.info("[WalterRouter] preview 조회 중단 — 최근 업로드 기록 없음")
        return {"count": 0, "items": []}

    df = await _walter_use_case.preview_uploaded_rows(session)
    if not df.empty and "PassengerId" in df.columns:
        df = df[df["PassengerId"].isin(last_uploaded_ids)]
    items = df.to_dict(orient="records") if not df.empty else []
    log.info("[WalterRouter] preview 조회 완료 — rows=%s", len(items))
    return {"count": len(items), "items": items}
