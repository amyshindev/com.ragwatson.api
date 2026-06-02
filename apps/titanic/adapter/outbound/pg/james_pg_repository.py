from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.app.ports.output.james_repository import JamesRepository
from titanic.adapter.inbound.api.schemas.james_schema import JamesPassengerRow
from titanic.app.dtos.james_dto import PersonCommand, BookingCommand

class JamesPgRepository(JamesRepository):

    def __init__(self) -> None:
        pass

    async def receive_uploaded_records(self, 
                                       person_commands: list[PersonCommand],
                                       booking_commands: list[BookingCommand]) -> int:

        # person_commands와 booking_commands 로그를 출력하는 코드
        print("[JamesRepository] Personcommand 상위 5개 레코드:")
        for person in person_commands[:5]:
            print(person, flush=True)

        print("[JamesRepository] Bookingcommand 상위 5개 레코드:")
        for booking in booking_commands[:5]:
            print(booking, flush=True)

        return len(person_commands) + len(booking_commands)

