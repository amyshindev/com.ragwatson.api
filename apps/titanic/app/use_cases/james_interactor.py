from __future__ import annotations

import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import is_database_configured
from titanic.adapter.inbound.api.schemas.james_schema import JamesSchema
from titanic.app.dtos.james_dto import BookingCommand, PersonCommand
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.output.james_repository import JamesRepository

log = logging.getLogger(__name__)


def _parse_passenger_id(raw: str | None) -> int | None:
    text = (raw or "").strip()
    if not text:
        return None
    return int(text)


class JamesInteractor(JamesUseCase):
    def __init__(self, session: AsyncSession, repository: JamesRepository) -> None:
        self._session = session
        self._repository = repository

    async def upload_titanic_file(self, schema: list[JamesSchema]) -> dict[str, int]:
        if not is_database_configured():
            raise HTTPException(status_code=503, detail="DATABASE_URL is not set.")

        log.info("[JamesInteractor] upload_titanic_file 시작 — count=%s", len(schema))
        log.info("2️⃣  [JamesUseCase] 라우터에서 유스케이스로 옮겨진 스키마 상위 5개 레코드:")
        for record in schema[:5]:
            log.info("%s", record)

        person_commands: list[PersonCommand] = []
        booking_commands: list[BookingCommand] = []
        for record in schema:
            passenger_id = _parse_passenger_id(record.passenger_id)
            if passenger_id is None:
                continue
            person_commands.append(
                PersonCommand(
                    passenger_id=passenger_id,
                    name=record.name or "",
                    gender=record.gender or "",
                    age=record.age or "",
                    sib_sp=record.sibsp or "",
                    parch=record.parch or "",
                    survived=record.survived or "",
                )
            )
            booking_commands.append(
                BookingCommand(
                    pclass=record.pclass or "",
                    ticket=record.ticket or "",
                    fare=record.fare or "",
                    cabin=record.cabin or "",
                    embarked=record.embarked or "",
                )
            )

        try:
            saved = await self._repository.receive_uploaded_records(
                person_commands,
                booking_commands,
            )
            await self._session.commit()
        except HTTPException:
            await self._session.rollback()
            raise
        except Exception:
            await self._session.rollback()
            raise

        log.info("[JamesInteractor] upload_titanic_file 완료 — saved=%s", saved)
        return {"saved": saved}
