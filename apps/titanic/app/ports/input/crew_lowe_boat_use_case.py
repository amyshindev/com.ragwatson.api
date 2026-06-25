from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatResponse


class LoweBoatUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
        """로우 보트의 자기소개 메소드"""
        pass

    @abstractmethod
    def split_dataset(
        self, df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """전체 데이터셋을 train / test 로 분리하는 메서드.
        test set 이 DB 에 없을 때 Smith 가 호출한다.
        """
        pass


CrewLoweBoatUseCase = LoweBoatUseCase
