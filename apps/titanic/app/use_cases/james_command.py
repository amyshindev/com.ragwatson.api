from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.output.james_repository import JamesRepository

log = logging.getLogger(__name__)


class JamesCommandUseCase(JamesUseCase):
    """입력 포트 구현 — 업로드 데이터를 출력 포트(JamesPgRepository)로 전달."""

    def __init__(
        self,
        session: AsyncSession,
        filename: str,
        repository: JamesRepository | None = None,
    ) -> None:
        self._session = session
        self._filename = filename
        self._repository = repository

    async def receive_uploaded_records(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        log.info(
            "[JamesCommandUseCase] receive_uploaded_records — filename=%s rows=%s",
            self._filename,
            len(records),
        )
        repository = self._repository or JamesPgRepository(self._session)
        count = await repository.save_all(records)
        rows = [
            {str(k): str(v) if v is not None else "" for k, v in record.items()}
            for record in records
        ]
        log.info("[JamesCommandUseCase] 완료 — filename=%s count=%s", self._filename, count)
        return {
            "filename": self._filename,
            "count": count,
            "items": rows,
        }
