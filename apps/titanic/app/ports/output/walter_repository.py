from abc import ABC, abstractmethod

from titanic.app.dtos.walter_dto import WalterQuery


class WalterRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: WalterQuery) -> None:
        ...
