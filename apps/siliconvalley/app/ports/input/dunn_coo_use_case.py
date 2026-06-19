from __future__ import annotations

from abc import ABC, abstractmethod

from siliconvalley.adapter.inbound.api.schemas.dunn_coo_schema import DunnCooSchema
from siliconvalley.app.dtos.dunn_coo_dto import DunnCooResponse


class DunnCooUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: DunnCooSchema) -> DunnCooResponse:
        pass
