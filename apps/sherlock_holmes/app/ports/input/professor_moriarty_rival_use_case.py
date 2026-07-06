from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_holmes.adapter.inbound.api.schemas.professor_moriarty_rival_schema import MoriartyRivalSchema
from sherlock_holmes.app.dtos.professor_moriarty_rival_dto import MoriartyRivalResponse


class MoriartyRivalUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: MoriartyRivalSchema) -> MoriartyRivalResponse:
        """모리어티 자기소개"""
        pass


ProfessorMoriartyRivalUseCase = MoriartyRivalUseCase
