from abc import ABC, abstractmethod

from titanic.app.dtos.walter_dto import WalterQuery

class WalterRepository(ABC):
    # 월터의 승객 명단 관리 저장소

    @abstractmethod
    def introduce_myself(self, query: WalterQuery):
        pass
