from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.walter_pg_repository import WalterPgRepository
from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.ports.output.walter_repository import WalterRepository

log = logging.getLogger(__name__)


class WalterInteractor(WalterUseCase):
    """입력 포트 구현 — preview 조회를 출력 포트(WalterPgRepository)로 위임."""

    def __init__(
        self,
        session: AsyncSession,
        repository: WalterRepository | None = None,
    ) -> None:
        self._session = session
        self._repository = repository

    async def get_preview_records(self, passenger_ids: list[int]) -> dict[str, Any]:
        log.info(
            "[WalterInteractor] get_preview_records — passenger_ids=%s",
            len(passenger_ids),
        )
        repository = self._repository or WalterPgRepository(self._session)
        all_records = await repository.find_all()
        if not passenger_ids:
            log.info("[WalterInteractor] 전체 조회 반환 — rows=%s", len(all_records))
            return {"count": len(all_records), "items": all_records}

        id_set = set(passenger_ids)
        items = [record for record in all_records if record.get("PassengerId") in id_set]
        log.info("[WalterInteractor] 완료 — rows=%s", len(items))
        return {"count": len(items), "items": items}
