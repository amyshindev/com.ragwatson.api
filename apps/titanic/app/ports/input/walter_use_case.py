from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class WalterUseCase(ABC):
    @abstractmethod
    async def get_preview_records(self, passenger_ids: list[int]) -> dict[str, Any]:
        ...
