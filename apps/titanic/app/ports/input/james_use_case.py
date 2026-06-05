from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.james_schema import JamesSchema


class JamesUseCase(ABC):
    @abstractmethod
    async def upload_titanic_file(self, schema: list[JamesSchema]) -> dict[str, int]:
        """파싱된 타이타닉 CSV 레코드를 저장한다."""
        ...
