from __future__ import annotations

import logging

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.booking_orm import BookingOrm
from titanic.adapter.outbound.orm.person_orm import PersonOrm
from titanic.app.dtos.james_dto import BookingCommand, PersonCommand
from titanic.app.ports.output.james_repository import JamesRepository

log = logging.getLogger(__name__)

_BATCH_SIZE = 500


def _person_row(command: PersonCommand) -> dict[str, str | int]:
    return {
        "passenger_id": command.passenger_id,
        "name": command.name,
        "gender": command.gender,
        "age": command.age,
        "sib_sp": command.sib_sp,
        "parch": command.parch,
        "survived": command.survived,
    }


def _booking_row(passenger_id: int, command: BookingCommand) -> dict[str, str | int]:
    return {
        "passenger_id": passenger_id,
        "pclass": command.pclass,
        "ticket": command.ticket,
        "fare": command.fare,
        "cabin": command.cabin,
        "embarked": command.embarked,
    }


class JamesPgRepository(JamesRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def receive_uploaded_records(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        if len(person_commands) != len(booking_commands):
            raise ValueError("person_commands와 booking_commands 길이가 일치해야 합니다.")
        if not person_commands:
            return 0

        log.info("3️⃣  [JamesRepository] PersonCommand 상위 5개 레코드:")
        for person in person_commands[:5]:
            log.info("%s", person)
        log.info("3️⃣  [JamesRepository] BookingCommand 상위 5개 레코드:")
        for booking in booking_commands[:5]:
            log.info("%s", booking)

        passenger_ids = [cmd.passenger_id for cmd in person_commands]

        for start in range(0, len(person_commands), _BATCH_SIZE):
            chunk = person_commands[start : start + _BATCH_SIZE]
            insert_stmt = pg_insert(PersonOrm).values([_person_row(cmd) for cmd in chunk])
            upsert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=[PersonOrm.passenger_id],
                set_={
                    "name": insert_stmt.excluded.name,
                    "gender": insert_stmt.excluded.gender,
                    "age": insert_stmt.excluded.age,
                    "sib_sp": insert_stmt.excluded.sib_sp,
                    "parch": insert_stmt.excluded.parch,
                    "survived": insert_stmt.excluded.survived,
                },
            )
            await self._session.execute(upsert_stmt)

        if passenger_ids:
            await self._session.execute(
                delete(BookingOrm).where(BookingOrm.passenger_id.in_(passenger_ids))
            )

        booking_rows = [
            _booking_row(person_cmd.passenger_id, booking_cmd)
            for person_cmd, booking_cmd in zip(person_commands, booking_commands, strict=True)
        ]

        for start in range(0, len(booking_rows), _BATCH_SIZE):
            chunk = booking_rows[start : start + _BATCH_SIZE]
            await self._session.execute(pg_insert(BookingOrm).values(chunk))

        count = len(person_commands)
        log.info("[JamesPgRepository] receive_uploaded_records 완료 — rows=%s", count)
        return count
