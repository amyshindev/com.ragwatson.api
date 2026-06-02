from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from titanic.adapter.inbound.api.schemas.james_schema import JamesPassengerRow


class JamesUseCase(ABC):

    @abstractmethod
    async def receive_uploaded_records(self, schema: list[JamesPassengerRow]):
        """CSV 파일업로드 """
        ...