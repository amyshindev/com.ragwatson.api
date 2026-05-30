import csv
import io
import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

import database
from core.config import is_database_configured
from db.session import DbSession
from titanic.app.use_cases.james_command import JamesCommandUseCase

log = logging.getLogger(__name__)

james_router = APIRouter(prefix="/api/james/v1", tags=["james"])
_LAST_UPLOADED_PASSENGER_IDS: list[int] = []

_REQUIRED_COLUMNS = {
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
}

_COLUMN_ORDER = [
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "Gender",
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
]


def get_last_uploaded_passenger_ids() -> list[int]:
    return list(_LAST_UPLOADED_PASSENGER_IDS)


@james_router.post("/upload")
async def upload_james_csv(session: DbSession, file: UploadFile = File(...)) -> dict:
    log.info("[JamesRouter] upload 시작 — filename=%s", file.filename)
    if not is_database_configured():
        raise HTTPException(status_code=503, detail="DATABASE_URL is not set.")
    # 사용자가 테이블을 수동 drop한 경우를 대비해 업로드 직전에 테이블 존재를 보장한다.
    from orm_registry import import_all_models

    import_all_models()
    await database.init_db()

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    content = await file.read()
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="UTF-8 CSV 파일만 지원합니다.",
        ) from exc

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV 헤더를 찾을 수 없습니다.")

    missing = sorted(_REQUIRED_COLUMNS - set(reader.fieldnames))
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"필수 컬럼이 없습니다: {', '.join(missing)}",
        )

    rows: list[dict[str, str]] = []
    for row in reader:
        normalized = {
            "PassengerId": str(row.get("PassengerId", "") or ""),
            "Survived": str(row.get("Survived", "") or ""),
            "Pclass": str(row.get("Pclass", "") or ""),
            "Name": str(row.get("Name", "") or ""),
            "Gender": str(row.get("Sex", "") or ""),
            "Age": str(row.get("Age", "") or ""),
            "SibSp": str(row.get("SibSp", "") or ""),
            "Parch": str(row.get("Parch", "") or ""),
            "Ticket": str(row.get("Ticket", "") or ""),
            "Fare": str(row.get("Fare", "") or ""),
            "Cabin": str(row.get("Cabin", "") or ""),
            "Embarked": str(row.get("Embarked", "") or ""),
        }
        rows.append(normalized)
    log.info("[JamesRouter] CSV 파싱 완료 — filename=%s rows=%s", file.filename, len(rows))
    last_uploaded_ids: list[int] = []
    for row in rows:
        try:
            last_uploaded_ids.append(int(row.get("PassengerId", "")))
        except ValueError:
            continue

    try:
        use_case = JamesCommandUseCase(session, file.filename or "")
        result = await use_case.receive_uploaded_records(rows)
        await session.commit()
        global _LAST_UPLOADED_PASSENGER_IDS
        _LAST_UPLOADED_PASSENGER_IDS = last_uploaded_ids
        log.info("[JamesRouter] commit 완료 — filename=%s rows=%s", file.filename, len(rows))
    except HTTPException:
        await session.rollback()
        raise
    except Exception as exc:
        await session.rollback()
        log.exception("james csv upload failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "filename": result["filename"],
        "count": result["count"],
        "columns": _COLUMN_ORDER,
        "items": result["items"],
    }
