from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.db_init import ensure_titanic_schema
from titanic.app.ports.output.james_repository import JamesRepository
from titanic.adapter.outbound.orm.titanic_model import Passenger

log = logging.getLogger(__name__)


def _optional_str(value: str) -> str | None:
    return value if value else None


def _optional_float(value: str) -> float | None:
    if not value:
        return None
    return float(value)


def _row_to_payload(row: dict[str, str]) -> dict:
    return {
        "passenger_id": int(row["PassengerId"]),
        "survived": int(row["Survived"]),
        "pclass": int(row["Pclass"]),
        "name": row["Name"],
        "sex": row["Gender"],
        "age": _optional_float(row.get("Age", "")),
        "sibsp": int(row["SibSp"]),
        "parch": int(row["Parch"]),
        "ticket": row["Ticket"],
        "fare": float(row["Fare"]),
        "cabin": _optional_str(row.get("Cabin", "")),
        "boat": None,
        "embarked": _optional_str(row.get("Embarked", "")),
    }


class JamesPgRepository(JamesRepository):
    """James 출력 포트 구현 — Neon DB(passengers)에 저장."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_all(self, records: list[dict[str, Any]]) -> int:
        await ensure_titanic_schema()
        rows = [
            {str(k): str(v) if v is not None else "" for k, v in record.items()}
            for record in records
        ]
        items = list(rows)
        payloads = [_row_to_payload(row) for row in items]
        if payloads:
            stmt = insert(Passenger).values(payloads)
            upsert_stmt = stmt.on_conflict_do_update(
                index_elements=[Passenger.passenger_id],
                set_={
                    "survived": stmt.excluded.survived,
                    "pclass": stmt.excluded.pclass,
                    "name": stmt.excluded.name,
                    "sex": stmt.excluded.sex,
                    "age": stmt.excluded.age,
                    "sibsp": stmt.excluded.sibsp,
                    "parch": stmt.excluded.parch,
                    "ticket": stmt.excluded.ticket,
                    "fare": stmt.excluded.fare,
                    "cabin": stmt.excluded.cabin,
                    "boat": stmt.excluded.boat,
                    "embarked": stmt.excluded.embarked,
                },
            )
            await self._session.execute(upsert_stmt)
        await self._session.flush()
        log.info("[JamesPgRepository] save_all 완료 — count=%s", len(items))
        return len(items)
