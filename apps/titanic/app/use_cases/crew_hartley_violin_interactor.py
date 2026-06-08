from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import CrewHartleyViolinSchema
from titanic.app.dtos.crew_hartley_violin_dto import CrewHartleyViolinQuery, CrewHartleyViolinResponse
from titanic.app.ports.input.crew_hartley_violin_use_case import CrewHartleyViolinUseCase
from titanic.app.ports.output.crew_hartley_violin_repository import CrewHartleyViolinRepository


class CrewHartleyViolinInteractor(CrewHartleyViolinUseCase):

    def __init__(self, repository: CrewHartleyViolinRepository):
        self.repository = repository

    async def introduce_myself(self, schema: CrewHartleyViolinSchema) -> CrewHartleyViolinResponse:
        '''하틀리 바이올리니스트의 자기소개 인터렉트'''
        query = CrewHartleyViolinQuery(
            id = schema.id,
            name = schema.name
        )
        return await self.repository.introduce_myself(query)
