from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import PassengerMollyScalerSchema
from titanic.app.dtos.passenger_molly_scaler_dto import PassengerMollyScalerQuery, PassengerMollyScalerResponse
from titanic.app.ports.input.passenger_molly_scaler_use_case import PassengerMollyScalerUseCase
from titanic.app.ports.output.passenger_molly_scaler_repository import PassengerMollyScalerRepository


class PassengerMollyScalerInteractor(PassengerMollyScalerUseCase):

    def __init__(self, repository: PassengerMollyScalerRepository):
        self.repository = repository

    async def introduce_myself(self, schema: PassengerMollyScalerSchema) -> PassengerMollyScalerResponse:
        '''몰리 스케일러의 자기소개 인터렉트'''
        query = PassengerMollyScalerQuery(
            id = schema.id,
            name = schema.name
        )
        return await self.repository.introduce_myself(query)
