from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository


class JackTrainerInteractor(JackTrainerUseCase):
    
    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''\uc7ad \ud2b8\ub808\uc774\ub108\uc758 \uc790\uae30\uc18c\uac1c \uc778\ud130\ub809\ud2b8'''

        return await self.repository.introduce_myself(JackTrainerQuery(
            id = schema.id,
            name = schema.name
        ))


PassengerJackTrainerInteractor = JackTrainerInteractor
