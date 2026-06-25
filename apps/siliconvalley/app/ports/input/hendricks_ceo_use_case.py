from __future__ import annotations

from abc import ABC, abstractmethod

from siliconvalley.adapter.inbound.api.schemas.hendricks_ceo_schema import HendricksCeoSchema
from siliconvalley.app.dtos.hendricks_ceo_dto import HendricksCeoResponse


class HendricksCeoUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: HendricksCeoSchema) -> HendricksCeoResponse:
        pass
