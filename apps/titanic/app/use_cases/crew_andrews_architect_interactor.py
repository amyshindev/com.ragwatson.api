from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import CrewAndrewsArchitectSchema
from titanic.app.dtos.crew_andrews_architect_dto import CrewAndrewsArchitectQuery, CrewAndrewsArchitectResponse
from titanic.app.ports.input.crew_andrews_architect_use_case import CrewAndrewsArchitectUseCase
from titanic.app.ports.output.crew_andrews_architect_repository import CrewAndrewsArchitectRepository


class CrewAndrewsArchitectInteractor(CrewAndrewsArchitectUseCase):
    
    def __init__(self, repository: CrewAndrewsArchitectRepository):
        self.repository = repository

    async def introduce_myself(self, schema: CrewAndrewsArchitectSchema) -> CrewAndrewsArchitectResponse:
        '''앤드류 아키텍트의 자기소개 인터렉트'''
        query = CrewAndrewsArchitectQuery(
            id = schema.id,
            name = schema.name
        )
        return await self.repository.introduce_myself(query)