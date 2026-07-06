from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_holmes.adapter.inbound.api.schemas.mrs_hudson_housekeeper_schema import HudsonHousekeeperSchema
from sherlock_holmes.app.dtos.mrs_hudson_housekeeper_dto import HudsonHousekeeperResponse


class HudsonHousekeeperUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: HudsonHousekeeperSchema) -> HudsonHousekeeperResponse:
        """허드슨 자기소개"""
        pass


MrsHudsonHousekeeperUseCase = HudsonHousekeeperUseCase
