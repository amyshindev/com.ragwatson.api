from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class WalterRepository(ABC):
    @abstractmethod
    async def find_all(self) -> list[dict[str, Any]]:
        ...
