from __future__ import annotations

import logging

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.output.crew_walter_roaster_port import WalterRoasterPort
from titanic.app.use_cases.crew_walter_roaster_reader import WalterReader

log = logging.getLogger(__name__)


class WalterRoasterPgRepository(WalterRoasterPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._reader = WalterReader()

    async def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        '''월터 로스터의 자기 소개 레포지토리 구현 메소드'''
        log.info("[WalterRoasterPgRepository] introduce_myself id=%s", query.id)
        return WalterRoasterResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )

    def get_train_set(self) -> pd.DataFrame:
        '''Survived 컬럼이 있는 데이터 전체를 데이터프레임으로 반환하는 메소드'''
        dataset = self._reader.get_dataset()
        if dataset.empty or "Survived" not in dataset.columns:
            log.warning("[WalterRoasterPgRepository] get_train_set | Survived 컬럼 없음")
            return pd.DataFrame()

        train_set = dataset.copy()
        log.info("[WalterRoasterPgRepository] get_train_set | rows=%s", len(train_set))
        return train_set

    def get_test_set(self) -> pd.DataFrame:
        '''Survived 컬럼이 없는 데이터 전체를 데이터프레임으로 반환하는 메소드'''
        dataset = self._reader.get_dataset()
        if dataset.empty:
            log.warning("[WalterRoasterPgRepository] get_test_set | 데이터 없음")
            return pd.DataFrame()

        test_set = dataset.drop(columns=["Survived"], errors="ignore").copy()
        log.info("[WalterRoasterPgRepository] get_test_set | rows=%s", len(test_set))
        return test_set


CrewWalterRoasterPgRepository = WalterRoasterPgRepository
