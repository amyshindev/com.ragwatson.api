from __future__ import annotations

from abc import ABC, abstractmethod

from siliconvalley.adapter.inbound.api.schemas.bighetti_hr_schema import BighettiHrSchema
from siliconvalley.app.dtos.bighetti_hr_dto import BighettiHrResponse


class BighettiHrUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: BighettiHrSchema) -> BighettiHrResponse:
        pass
