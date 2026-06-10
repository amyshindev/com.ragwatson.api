from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import CrewJamesDirectorSchema
from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.crew_james_director_repository import JamesDirectorRepository
from titanic.app.dtos.crew_james_director_dto import BookingCommand, PersonCommand


def _parse_passenger_id(raw: str | None) -> str | None:
    text = (raw or "").strip()
    if not text:
        return None
    return text


class JamesDirectorInteractor(JamesDirectorUseCase):
    def __init__(self, session: AsyncSession, repository: JamesDirectorRepository) -> None:
        self._session = session
        self.repository = repository

    async def upload_titanic_file(self, schema: list[CrewJamesDirectorSchema]) -> dict[str, int]:
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
            saved = await self.repository.receive_uploaded_records(person_commands, booking_commands)
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise
        return {"saved": saved}