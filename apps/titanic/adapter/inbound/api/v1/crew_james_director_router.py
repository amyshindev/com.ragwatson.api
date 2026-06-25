from __future__ import annotations

import csv
from io import StringIO
import logging
from typing import Any

from db.session import DbSession
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import CrewJamesDirectorSchema
from titanic.app.ports.input.crew_james_director_use_case import CrewJamesDirectorUseCase
from titanic.dependencies.crew_james_director_provider import get_crew_james_director_use_case

log = logging.getLogger(__name__)

_ALLOWED_CONTENT_TYPES = {"text/csv", "application/vnd.ms-excel", "text/plain"}

crew_james_director_router = APIRouter(prefix="/api/james/v1", tags=["james"])


@crew_james_director_router.post("/upload")
async def upload_titanic_csv(
    file: UploadFile = File(...),
    james: CrewJamesDirectorUseCase = Depends(get_crew_james_director_use_case),
) -> dict[str, str | int]:
    log.info("[CrewJamesDirectorRouter] upload start filename=%s", file.filename)
    if file.content_type not in _ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="CSV \ud30c\uc77c\uc744 \uc5c5\ub85c\ub4dc\ud574\uc8fc\uc138\uc694.",
        )

    schema = _parse_csv((await file.read()).decode("utf-8", errors="replace"))
    log.info(
        "1\ufe0f\u20e3  [CrewJamesDirectorRouter] "
        "\uc5c5\ub85c\ub4dc\ub41c CSV \ud30c\uc77c\uc5d0\uc11c \uc2a4\ud0a4\ub9c8\ub85c \uc62e\uaca8\uc9c4 "
        "\uc0c1\uc704 5\uac1c \ub808\ucf54\ub4dc (\uc804\uccb4 %s\uac74):",
        len(schema),
    )
    for record in schema[:5]:
        log.info("%s", record)

    result = await james.upload_titanic_file(schema)
    return {"filename": file.filename or "", **result}


def _parse_csv(text: str) -> list[CrewJamesDirectorSchema]:
    if not text.strip():
        raise HTTPException(status_code=400, detail="\ube48 CSV \ud30c\uc77c\uc785\ub2c8\ub2e4.")
    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")
    return [CrewJamesDirectorSchema(**_normalize_titanic_row(row)) for row in reader]


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


@crew_james_director_router.get("/passengers")
async def list_passengers(
    session: DbSession,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    raise HTTPException(status_code=501, detail="승객 조회 기능은 아직 구현되지 않았습니다.")
