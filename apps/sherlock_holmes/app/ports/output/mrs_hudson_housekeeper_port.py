from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_holmes.app.dtos.mrs_hudson_housekeeper_dto import HudsonHousekeeperQuery, HudsonHousekeeperResponse


class HudsonHousekeeperPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: HudsonHousekeeperQuery) -> HudsonHousekeeperResponse:
        """허드슨 자기소개 저장소"""
        pass


MrsHudsonHousekeeperPort = HudsonHousekeeperPort
