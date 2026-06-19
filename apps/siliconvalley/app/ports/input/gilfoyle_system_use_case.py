from __future__ import annotations

from abc import ABC, abstractmethod

from siliconvalley.adapter.inbound.api.schemas.gilfoyle_system_schema import GilfoyleSystemSchema
from siliconvalley.app.dtos.gilfoyle_system_dto import GilfoyleSystemResponse


class GilfoyleSystemUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: GilfoyleSystemSchema) -> GilfoyleSystemResponse:
        pass
