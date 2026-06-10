from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse


class WalterRoasterRepository(ABC):
    
    @abstractmethod
    async def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        '''월터 로스터의 자기 소개 레포지토리 추상 메소드'''
        pass


CrewWalterRoasterRepository = WalterRoasterRepository
