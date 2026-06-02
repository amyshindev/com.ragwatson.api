from __future__ import annotations

from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.output.james_repository import JamesRepository

from titanic.adapter.inbound.api.schemas.james_schema import JamesPassengerRow
from titanic.app.dtos.james_dto import PersonCommand, BookingCommand
from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository


class JamesInteractor(JamesUseCase):
    def __init__(self) -> None:
        pass

    async def receive_uploaded_records(self, schema: list[JamesPassengerRow]) -> None:
        print("[JamesUseCase] 라우터에서 유스케이스로 옮겨진 스키마 상위 5개 레코드:")
        for record in schema[:5]:
            print(record)

        # schema를 PersonCommand와 BookingCommand로 나눠서 옮겨담기
        person_commands: list[PersonCommand] = []
        booking_commands: list[BookingCommand] = []

        for record in schema:
            person_commands.append(PersonCommand(
                passenger_id=record.passenger_id or "",
                name=record.name or "",
                gender=record.gender or "",
                age=record.age or "",
                sib_sp=record.sibsp or "",
                parch=record.parch or "",
                survived=record.survived or "",
            ))
            booking_commands.append(BookingCommand(
                pclass=record.pclass or "",
                ticket=record.ticket or "",
                fare=record.fare or "",
                cabin=record.cabin or "",
                embarked=record.embarked or "",
            ))

        repository: JamesRepository = JamesPgRepository()

        await repository.receive_uploaded_records(person_commands, booking_commands)

        pass