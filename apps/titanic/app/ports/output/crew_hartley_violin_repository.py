from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse


class HartleyViolinRepository(ABC):
    
    @abstractmethod
    async def introduce_myself(self, query: HartleyViolinQuery) -> HartleyViolinResponse:
        '''하틀리 바이올리니스트의 자기 소개 레포지토리 추상 메소드'''
        pass


CrewHartleyViolinRepository = HartleyViolinRepository
