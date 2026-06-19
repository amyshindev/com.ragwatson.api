from __future__ import annotations

from abc import ABC, abstractmethod

from siliconvalley.app.dtos.bighetti_hr_dto import BighettiHrQuery, BighettiHrResponse


class BighettiHrPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: BighettiHrQuery) -> BighettiHrResponse:
        pass
