from __future__ import annotations

from abc import ABC, abstractmethod

from automata.adapter.inbound.api.schemas.ford_director_schema import (
    FordDirectorSchema,
    FordDirectorTriggerSchema,
)
from automata.app.dtos.ford_director_dto import FordDirectorResponse


class FordDirectorUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: FordDirectorSchema) -> FordDirectorResponse:
        pass

    @abstractmethod
    async def trigger_workflow(self, schema: FordDirectorTriggerSchema) -> FordDirectorResponse:
        pass
