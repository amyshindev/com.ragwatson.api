from __future__ import annotations

from abc import ABC, abstractmethod

from siliconvalley.adapter.inbound.api.schemas.dinesh_dash_schema import DineshDashSchema
from siliconvalley.app.dtos.dinesh_dash_dto import DineshDashResponse


class DineshDashUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: DineshDashSchema) -> DineshDashResponse:
        pass
