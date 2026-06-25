from abc import ABC, abstractmethod
from uuid import UUID

from audio.adapter.inbound.api.schemas.generation_logs import (
    GenerationLogCreate,
    GenerationLogRead,
    GenerationLogStatusRead,
)


class GenerationLogUseCase(ABC):
    @abstractmethod
    async def log_generation(self, body: GenerationLogCreate) -> GenerationLogRead: ...

    @abstractmethod
    async def get(self, generation_id: UUID) -> GenerationLogRead: ...

    @abstractmethod
    async def get_status(self, generation_id: UUID) -> GenerationLogStatusRead: ...

    @abstractmethod
    async def list_by_user(
        self,
        user_id: int,
        status: str | None,
        limit: int,
        offset: int,
    ) -> list[GenerationLogRead]: ...

    @abstractmethod
    async def update_result(self, generation_id: UUID, result: dict) -> GenerationLogRead: ...

    @abstractmethod
    async def update_loop_meta(self, generation_id: UUID, meta: dict) -> GenerationLogRead: ...
