from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import CrewWalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import CrewWalterRoasterQuery, CrewWalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import CrewWalterRoasterUseCase
from titanic.app.ports.output.crew_walter_roaster_repository import CrewWalterRoasterRepository


class CrewWalterRoasterInteractor(CrewWalterRoasterUseCase):

    def __init__(self, repository: CrewWalterRoasterRepository):
        self.repository = repository

    async def introduce_myself(self, schema: CrewWalterRoasterSchema) -> CrewWalterRoasterResponse:
        '''월터 로스터의 자기소개 인터렉트'''
        query = CrewWalterRoasterQuery(
            id = schema.id,
            name = schema.name
        )
        return await self.repository.introduce_myself(query)
