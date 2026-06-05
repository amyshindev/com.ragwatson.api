from abc import ABC, abstractmethod
from uuid import UUID

from audio.adapter.inbound.api.schemas.generation_logs import GenerationLogCreate
from audio.adapter.outbound.orm.generation_log_orm import GenerationLog


class GenerationLogRepository(ABC):
    @abstractmethod
    async def create(self, body: GenerationLogCreate) -> GenerationLog:
        ...

    @abstractmethod
    async def get(self, generation_id: UUID) -> GenerationLog | None:
        ...

    @abstractmethod
    async def list_by_user(
        self,
        user_id: int,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[GenerationLog]:
        ...

    @abstractmethod
    async def update_result(
        self, generation_id: UUID, result: dict
    ) -> GenerationLog:
        ...

    @abstractmethod
    async def update_loop_meta(
        self, generation_id: UUID, meta: dict
    ) -> GenerationLog:
        ...
