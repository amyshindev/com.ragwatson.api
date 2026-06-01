from __future__ import annotations

import csv
import io
import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.output.james_repository import JamesRepository

log = logging.getLogger(__name__)

_LAST_UPLOADED_PASSENGER_IDS: list[int] = []

_REQUIRED_COLUMNS = {
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
}

_GENDER_COLUMNS = {"Gender", "Sex"}


def get_last_uploaded_passenger_ids() -> list[int]:
    return list(_LAST_UPLOADED_PASSENGER_IDS)


class JamesInteractor(JamesUseCase):
    """입력 포트 구현 — CSV 변환, 저장 orchestration, 트랜잭션."""

    def __init__(
        self,
        session: AsyncSession,
        filename: str,
        repository: JamesRepository,
    ) -> None:
        self._session = session
        self._filename = filename
        self._repository = repository

    @staticmethod
    def parse_upload_csv(filename: str | None, content: bytes) -> list[dict[str, str]]:
        if not filename or not filename.lower().endswith(".csv"):
            raise ValueError("CSV 파일만 업로드할 수 있습니다.")
        try:
            text = content.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ValueError("UTF-8 CSV 파일만 지원합니다.") from exc

        reader = csv.DictReader(io.StringIO(text))
        if not reader.fieldnames:
            raise ValueError("CSV 헤더를 찾을 수 없습니다.")

        fieldnames = set(reader.fieldnames)
        missing = sorted(_REQUIRED_COLUMNS - fieldnames)
        if missing:
            raise ValueError(f"필수 컬럼이 없습니다: {', '.join(missing)}")
        if not _GENDER_COLUMNS & fieldnames:
            raise ValueError("필수 컬럼이 없습니다: Gender (또는 Sex)")

        rows: list[dict[str, str]] = []
        for row in reader:
            rows.append(
                {
                    "PassengerId": str(row.get("PassengerId", "") or ""),
                    "Survived": str(row.get("Survived", "") or ""),
                    "Pclass": str(row.get("Pclass", "") or ""),
                    "Name": str(row.get("Name", "") or ""),
                    "Gender": str(row.get("Gender") or row.get("Sex", "") or ""),
                    "Age": str(row.get("Age", "") or ""),
                    "SibSp": str(row.get("SibSp", "") or ""),
                    "Parch": str(row.get("Parch", "") or ""),
                    "Ticket": str(row.get("Ticket", "") or ""),
                    "Fare": str(row.get("Fare", "") or ""),
                    "Cabin": str(row.get("Cabin", "") or ""),
                    "Embarked": str(row.get("Embarked", "") or ""),
                }
            )
        return rows

    async def receive_uploaded_records(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        log.info(
            "[JamesInteractor] receive_uploaded_records — filename=%s rows=%s",
            self._filename,
            len(records),
        )
        rows = [
            {str(k): str(v) if v is not None else "" for k, v in record.items()}
            for record in records
        ]
        try:
            count = await self._repository.save_all(rows)
            global _LAST_UPLOADED_PASSENGER_IDS
            _LAST_UPLOADED_PASSENGER_IDS = self._extract_passenger_ids(rows)
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise

        log.info("[JamesInteractor] 완료 — filename=%s count=%s", self._filename, count)
        return {
            "filename": self._filename,
            "count": count,
            "items": rows,
        }

    @staticmethod
    def _extract_passenger_ids(rows: list[dict[str, str]]) -> list[int]:
        passenger_ids: list[int] = []
        for row in rows:
            try:
                passenger_ids.append(int(row.get("PassengerId", "")))
            except ValueError:
                continue
        return passenger_ids
