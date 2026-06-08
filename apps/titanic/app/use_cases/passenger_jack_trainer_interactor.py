from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import PassengerJackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import PassengerJackTrainerQuery, PassengerJackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import PassengerJackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import PassengerJackTrainerRepository


class PassengerJackTrainerInteractor(PassengerJackTrainerUseCase):

    def __init__(self, repository: PassengerJackTrainerRepository):
        self.repository = repository

    async def introduce_myself(self, schema: PassengerJackTrainerSchema) -> PassengerJackTrainerResponse:
        '''잭 트레이너의 자기소개 인터렉트'''
        query = PassengerJackTrainerQuery(
            id = schema.id,
            name = schema.name
        )
        return await self.repository.introduce_myself(query)
