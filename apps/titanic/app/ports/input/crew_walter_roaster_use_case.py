from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse


class WalterRoasterUseCase(ABC):
    @abstractmethod
    def get_train_set(self) -> pd.DataFrame:
        """Survived 컬럼이 있는 학습 데이터 전체를 반환한다"""

    @abstractmethod
    def get_test_set(self) -> pd.DataFrame:
        """Survived 컬럼이 없는 시험 데이터 전체를 반환한다"""

    @abstractmethod
    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        """월터 로스터의 자기소개 메소드"""
        pass


CrewWalterRoasterUseCase = WalterRoasterUseCase
