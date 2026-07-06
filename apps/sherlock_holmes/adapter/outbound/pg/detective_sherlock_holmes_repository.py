from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from sherlock_holmes.app.dtos.detective_sherlock_holmes_dto import SherlockHolmesQuery, SherlockHolmesResponse
from sherlock_holmes.app.ports.output.detective_sherlock_holmes_port import SherlockHolmesPort

log = logging.getLogger(__name__)


class SherlockHolmesPgRepository(SherlockHolmesPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: SherlockHolmesQuery) -> SherlockHolmesResponse:
        log.info("[SherlockHolmesPgRepository] introduce_myself id=%s", query.id)
        return SherlockHolmesResponse(
            id=query.id,
            name=f"{query.name} — 베이커가 221B, 추론·단서 분석",
        )


DetectiveSherlockHolmesPgRepository = SherlockHolmesPgRepository
