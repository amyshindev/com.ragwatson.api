from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import PassengerRoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import PassengerRoseModelQuery, PassengerRoseModelResponse
from titanic.app.ports.input.passenger_rose_model_use_case import PassengerRoseModelUseCase
from titanic.app.ports.output.passenger_rose_model_repository import PassengerRoseModelRepository


class PassengerRoseModelInteractor(PassengerRoseModelUseCase):

    def __init__(self, repository: PassengerRoseModelRepository):
        self.repository = repository

    async def introduce_myself(self, schema: PassengerRoseModelSchema) -> PassengerRoseModelResponse:
        '''로즈 모델의 자기소개 인터렉트'''
        query = PassengerRoseModelQuery(
            id = schema.id,
            name = schema.name
        )
        return await self.repository.introduce_myself(query)
