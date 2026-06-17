from __future__ import annotations

import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.output.crew_walter_roaster_port import WalterRoasterPort


class WalterRoasterInteractor(WalterRoasterUseCase):

    def __init__(self, repository: WalterRoasterPort):
        self.repository = repository

    def get_train_set(self) -> pd.DataFrame:
        '''월터가 train set을 가져오는 메소드'''
        return self.repository.get_train_set()

    def get_test_set(self) -> pd.DataFrame:
        '''월터가 test set을 가져오는 메소드'''
        return self.repository.get_test_set()

    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        '''월터 로스터의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(WalterRoasterQuery(
            id=schema.id,
            name=schema.name,
        ))


CrewWalterRoasterInteractor = WalterRoasterInteractor
