from __future__ import annotations
from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.james_schema import JamesSchema


class JamesUseCase(ABC):

    @abstractmethod
    async def receive_uploaded_records(self, schema: list[JamesSchema]) -> int:
        """CSV 파일업로드."""
        ...