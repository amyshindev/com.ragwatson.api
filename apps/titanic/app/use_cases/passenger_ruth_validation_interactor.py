from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import PassengerRuthValidationSchema
from titanic.app.dtos.passenger_ruth_validation_dto import PassengerRuthValidationQuery, PassengerRuthValidationResponse
from titanic.app.ports.input.passenger_ruth_validation_use_case import PassengerRuthValidationUseCase
from titanic.app.ports.output.passenger_ruth_validation_repository import PassengerRuthValidationRepository


class PassengerRuthValidationInteractor(PassengerRuthValidationUseCase):

    def __init__(self, repository: PassengerRuthValidationRepository):
        self.repository = repository

    async def introduce_myself(self, schema: PassengerRuthValidationSchema) -> PassengerRuthValidationResponse:
        '''루스 검증의 자기소개 인터렉트'''
        query = PassengerRuthValidationQuery(
            id = schema.id,
            name = schema.name
        )
        return await self.repository.introduce_myself(query)
