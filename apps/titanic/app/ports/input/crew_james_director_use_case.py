from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import CrewJamesDirectorSchema


class JamesDirectorUseCase(ABC):

    @abstractmethod
    async def upload_titanic_file(self, schema: list[CrewJamesDirectorSchema]) -> dict[str, int]:
        """CSV upload."""
        ...


CrewJamesDirectorUseCase = JamesDirectorUseCase