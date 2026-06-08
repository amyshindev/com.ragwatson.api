from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import CrewLoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import CrewLoweBoatQuery, CrewLoweBoatResponse
from titanic.app.ports.input.crew_lowe_boat_use_case import CrewLoweBoatUseCase
from titanic.app.ports.output.crew_lowe_boat_repository import CrewLoweBoatRepository


class CrewLoweBoatInteractor(CrewLoweBoatUseCase):

    def __init__(self, repository: CrewLoweBoatRepository):
        self.repository = repository

    async def introduce_myself(self, schema: CrewLoweBoatSchema) -> CrewLoweBoatResponse:
        '''로우 구명보트의 자기소개 인터렉트'''
        query = CrewLoweBoatQuery(
            id = schema.id,
            name = schema.name
        )
        return await self.repository.introduce_myself(query)
