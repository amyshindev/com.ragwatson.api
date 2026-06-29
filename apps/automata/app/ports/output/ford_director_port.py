from __future__ import annotations

from abc import ABC, abstractmethod

from automata.app.dtos.ford_director_dto import FordDirectorQuery, FordDirectorResponse


class FordDirectorPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: FordDirectorQuery) -> FordDirectorResponse:
        pass

    @abstractmethod
    async def trigger_workflow(self, query: FordDirectorQuery) -> FordDirectorResponse:
        pass
