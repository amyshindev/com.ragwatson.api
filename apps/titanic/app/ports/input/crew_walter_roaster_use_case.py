from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse


class WalterRoasterUseCase(ABC):

    @abstractmethod
    async def get_train_set(self) -> WalterRoasterResponse:
        '''월터가 DB에서 train set만 가져오는 메소드'''

    @abstractmethod
    async def get_test_set(self) -> WalterRoasterResponse:
        '''월터가 DB에서 test set만 가져오는 메소드'''

    @abstractmethod
    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        '''월터 로스터의 자기소개 메소드'''
        pass


CrewWalterRoasterUseCase = WalterRoasterUseCase
