from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse


class SmithCaptainUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 메소드'''
        pass

    @abstractmethod 
    async def chat_with_smith_captain(self, message: str) -> str:
        '''스미스 선장과의 대화 메소드'''
        pass

CrewSmithCaptainUseCase = SmithCaptainUseCase
