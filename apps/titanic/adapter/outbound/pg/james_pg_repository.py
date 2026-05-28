import logging
from collections.abc import Sequence

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.use_cases.passenger import Passenger

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


class JamesPgRepository:
    """James output port에서 전달된 업로드 데이터를 Neon DB(passengers)에 저장."""

    async def save_uploaded_rows(
        self,
        session: AsyncSession,
        filename: str,
        rows: Sequence[dict[str, str]],
    ) -> dict:
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
            await session.execute(upsert_stmt)
        await session.flush()
        log.info(
            "[JamesPgRepository] save_uploaded_rows 완료 — filename=%s count=%s",
            filename,
            len(items),
        )
        return {
            "filename": filename,
            "count": len(items),
            "items": items,
        }
