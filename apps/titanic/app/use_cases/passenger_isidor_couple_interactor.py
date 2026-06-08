from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import PassengerIsidorCoupleSchema
from titanic.app.dtos.passenger_isidor_couple_dto import PassengerIsidorCoupleQuery, PassengerIsidorCoupleResponse
from titanic.app.ports.input.passenger_isidor_couple_use_case import PassengerIsidorCoupleUseCase
from titanic.app.ports.output.passenger_isidor_couple_repository import PassengerIsidorCoupleRepository


class PassengerIsidorCoupleInteractor(PassengerIsidorCoupleUseCase):

    def __init__(self, repository: PassengerIsidorCoupleRepository):
        self.repository = repository

    async def introduce_myself(self, schema: PassengerIsidorCoupleSchema) -> PassengerIsidorCoupleResponse:
        '''이시도르 커플의 자기소개 인터렉트'''
        query = PassengerIsidorCoupleQuery(
            id = schema.id,
            name = schema.name
        )
        return await self.repository.introduce_myself(query)
