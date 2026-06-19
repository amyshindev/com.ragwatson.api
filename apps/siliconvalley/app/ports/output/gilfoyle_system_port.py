from __future__ import annotations

from abc import ABC, abstractmethod

from siliconvalley.app.dtos.gilfoyle_system_dto import GilfoyleSystemQuery, GilfoyleSystemResponse


class GilfoyleSystemPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: GilfoyleSystemQuery) -> GilfoyleSystemResponse:
        pass
