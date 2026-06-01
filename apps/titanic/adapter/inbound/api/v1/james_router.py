import logging

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import ValidationError

from core.config import is_database_configured
from db.session import DbSession
from titanic.adapter.inbound.api.schemas.james_schema import (
    JAMES_UPLOAD_COLUMNS,
    JamesPassengerRow,
    JamesUploadResponse,
)
from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic.app.use_cases.james_interactor import JamesInteractor

log = logging.getLogger(__name__)

james_router = APIRouter(prefix="/api/james/v1", tags=["james"])

# CSV 파일 업로드
@james_router.post("/upload", response_model=JamesUploadResponse)
async def upload_james_csv(session: DbSession, file: UploadFile = File(...)) -> JamesUploadResponse:
    log.info("[JamesRouter] upload 시작 — filename=%s", file.filename)
    if not is_database_configured():
        raise HTTPException(status_code=503, detail="DATABASE_URL is not set.")

    content = await file.read()
    try:
        raw_rows = JamesInteractor.parse_upload_csv(file.filename, content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    log.info("[JamesRouter] CSV 파싱 완료 — filename=%s rows=%s", file.filename, len(raw_rows))



    records: list[JamesPassengerRow] = []
    try:
        for raw_row in raw_rows:
            records.append(JamesPassengerRow.from_csv_row(raw_row))
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors()) from exc

    # records에 상위 5줄 출력하는 로그
    for index, record in enumerate(records[:5], start=1):
        log.info(
            "[JamesRouter] record sample %s/%s — %s",
            index,
            min(5, len(records)),
            record.model_dump(by_alias=True),
        )

    rows = [record.to_upload_row() for record in records]
    log.info(
        "[JamesRouter] 스키마 검증 완료 — filename=%s records=%s",
        file.filename,
        len(records),
    )

    use_case = JamesInteractor(
        session,
        file.filename or "",
        JamesPgRepository(session),
    )
    try:
        result = await use_case.receive_uploaded_records(rows)
    except HTTPException:
        raise
    except Exception as exc:
        log.exception("james csv upload failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    items = [record.to_upload_row() for record in records]
    log.info("[JamesRouter] upload 완료 — filename=%s rows=%s", file.filename, len(items))
    return JamesUploadResponse(
        filename=result["filename"],
        count=result["count"],
        columns=JAMES_UPLOAD_COLUMNS,
        items=items,
    )
