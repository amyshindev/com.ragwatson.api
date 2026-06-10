from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatResponse


class LoweBoatUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
        '''로우 구명보트의 자기소개 메소드'''
        pass


CrewLoweBoatUseCase = LoweBoatUseCase
