from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.walter_repository import WalterRepository
from titanic.adapter.outbound.orm.titanic_model import Passenger

log = logging.getLogger(__name__)


class WalterPgRepository(WalterRepository):
    """Walter 출력 포트 구현 — Neon DB(passengers)에서 조회."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_all(self) -> list[dict[str, Any]]:
        log.info("[WalterPgRepository] find_all 시작 — passengers")
        result = await self._session.execute(
            select(Passenger).order_by(Passenger.passenger_id.asc())
        )
        passengers = result.scalars().all()
        if not passengers:
            log.info("[WalterPgRepository] find_all 결과 없음")
            return []

        items = [
            {
                "PassengerId": p.passenger_id,
                "Survived": p.survived,
                "Pclass": p.pclass,
                "Name": p.name,
                "Sex": p.sex,
                "Age": p.age,
                "SibSp": p.sibsp,
                "Parch": p.parch,
                "Ticket": p.ticket,
                "Fare": p.fare,
                "Cabin": p.cabin,
                "Boat": p.boat,
                "Embarked": p.embarked,
            }
            for p in passengers
        ]
        log.info("[WalterPgRepository] find_all 완료 — rows=%s", len(items))
        return items
