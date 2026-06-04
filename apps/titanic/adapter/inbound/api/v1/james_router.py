import csv
from io import StringIO
import logging
from typing import Any

from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from core.config import is_database_configured
from db.session import DbSession

from titanic.adapter.inbound.api.schemas.james_schema import JamesSchema
from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic.app.use_cases.james_interactor import JamesInteractor
from titanic.app.ports.input.james_use_case import JamesUseCase


log = logging.getLogger(__name__)


james_router = APIRouter(prefix="/api/james/v1", tags=["james"])


@james_router.post("/upload")
async def upload_james_csv(session: DbSession, file: UploadFile = File(...)):
    log.info("[JamesRouter] upload 시작 — filename=%s", file.filename)
    if not is_database_configured():
        raise HTTPException(status_code=503, detail="DATABASE_URL is not set.")

    if file.content_type not in {"text/csv", "application/vnd.ms-excel", "text/plain"}:
        raise HTTPException(status_code=400, detail="CSV 파일을 업로드해주세요.")

    text = (await file.read()).decode("utf-8", errors="replace")
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")

    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")

    schema = [JamesSchema(**_normalize_titanic_row(row)) for row in reader]
    log.info("1️⃣  [JamesRouter] 업로드된 CSV 파일에서 스키마로 옮겨진 상위 5개 레코드 (전체 %s건):", len(schema))
    for record in schema[:5]:
        log.info("%s", record)

    try:
        use_case: JamesUseCase = JamesInteractor(session, JamesPgRepository(session))
        saved = await use_case.receive_uploaded_records(schema)
    except HTTPException:
        raise
    except Exception as exc:
        log.exception("james upload failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {"filename": file.filename, "saved": saved}


def _normalize_titanic_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        key = raw_key.strip()
        lower_key = key.lower()
        if lower_key == "sex":
            normalized["gender"] = value
        elif lower_key == "passengerid":
            normalized["passenger_id"] = value
        elif lower_key in {
            "passenger_id",
            "survived",
            "pclass",
            "name",
            "age",
            "sibsp",
            "parch",
            "ticket",
            "fare",
            "cabin",
            "embarked",
            "gender",
        }:
            normalized[lower_key] = value
    return normalized


@james_router.get("/passengers")
async def list_passengers(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    raise HTTPException(status_code=501, detail="승객 조회 기능은 아직 구현되지 않았습니다.")