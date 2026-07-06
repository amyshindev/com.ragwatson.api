from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_holmes.app.dtos.professor_moriarty_rival_dto import MoriartyRivalQuery, MoriartyRivalResponse


class MoriartyRivalPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: MoriartyRivalQuery) -> MoriartyRivalResponse:
        """모리어티 자기소개 저장소"""
        pass


ProfessorMoriartyRivalPort = MoriartyRivalPort
