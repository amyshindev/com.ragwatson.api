from __future__ import annotations

import csv
from io import StringIO
import logging
import re
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from automata.adapter.inbound.api.schemas.address_book_schema import (
    ContactListResponseSchema,
    ContactUploadRowSchema,
)
from automata.app.ports.input.address_book_use_case import AddressBookUseCase
from automata.dependencies.address_book_provider import get_address_book_use_case

log = logging.getLogger(__name__)

_ALLOWED_CONTENT_TYPES = {
    "text/csv",
    "application/vnd.ms-excel",
    "text/plain",
    "application/octet-stream",
}


def _accept_csv_upload(file: UploadFile) -> bool:
    content_type = (file.content_type or "").split(";")[0].strip().lower()
    if content_type in _ALLOWED_CONTENT_TYPES:
        return True
    filename = (file.filename or "").lower()
    return filename.endswith(".csv")

address_book_router = APIRouter(prefix="/automata/contacts", tags=["automata", "contacts"])


@address_book_router.post("/upload")
async def upload_contacts_csv(
    file: UploadFile = File(...),
    address_book: AddressBookUseCase = Depends(get_address_book_use_case),
) -> dict[str, str | int]:
    log.info("[AddressBookRouter] upload start filename=%s", file.filename)
    if not _accept_csv_upload(file):
        raise HTTPException(status_code=400, detail="CSV 파일을 업로드해주세요.")

    schema = _parse_csv((await file.read()).decode("utf-8-sig", errors="replace"))
    result = await address_book.upload_contacts(schema)
    return {"filename": file.filename or "", **result}


@address_book_router.get("", response_model=ContactListResponseSchema)
async def list_contacts(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    address_book: AddressBookUseCase = Depends(get_address_book_use_case),
) -> ContactListResponseSchema:
    return await address_book.list_contacts(page=page, page_size=page_size)


def _parse_csv(text: str) -> list[ContactUploadRowSchema]:
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")
    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")

    has_first_name = any(_is_first_name_column(name) for name in reader.fieldnames)
    has_email = any(_classify_contact_column(name) == "email" for name in reader.fieldnames)
    if not has_first_name or not has_email:
        missing: list[str] = []
        if not has_first_name:
            missing.append("First Name")
        if not has_email:
            missing.append("email")
        raise HTTPException(
            status_code=400,
            detail=f"CSV 헤더에 {', '.join(missing)} 컬럼을 찾을 수 없습니다.",
        )

    return [ContactUploadRowSchema(**_normalize_contact_row(row)) for row in reader]


def _normalize_contact_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        field = _classify_contact_column(raw_key)
        if field is not None:
            normalized[field] = value
    return normalized


def _normalize_header_key(raw_key: str) -> tuple[str, str]:
    key = raw_key.strip().lstrip("\ufeff").lower()
    key = re.sub(r"[\s\u00a0\u3000]+", " ", key).strip()
    compact = re.sub(r"[\s\-_]+", "", key)
    return key, compact


def _is_first_name_column(raw_key: str) -> bool:
    key, compact = _normalize_header_key(raw_key)
    return compact == "firstname" or key == "first name"


def _classify_contact_column(raw_key: str) -> str | None:
    """헤더에 First Name / email 관련 글자만 포함돼 있으면 매칭한다."""
    if _is_first_name_column(raw_key):
        return "nickname"

    key, compact = _normalize_header_key(raw_key)
    if "email" in compact or "이메일" in key or "mail" in compact:
        return "email"
    return None
