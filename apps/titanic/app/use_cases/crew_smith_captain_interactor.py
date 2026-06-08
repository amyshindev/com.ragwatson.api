from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import CrewSmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import CrewSmithCaptainQuery, CrewSmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import CrewSmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_repository import CrewSmithCaptainRepository


class CrewSmithCaptainInteractor(CrewSmithCaptainUseCase):

    def __init__(self, repository: CrewSmithCaptainRepository):
        self.repository = repository

    async def introduce_myself(self, schema: CrewSmithCaptainSchema) -> CrewSmithCaptainResponse:
        '''스미스 선장의 자기소개 인터렉트'''
        query = CrewSmithCaptainQuery(
            id = schema.id,
            name = schema.name
        )
        return await self.repository.introduce_myself(query)
