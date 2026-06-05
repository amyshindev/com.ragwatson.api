from abc import ABC, abstractmethod

from ml_data.adapter.inbound.api.schemas.user_events import UserEventCreate, UserEventRead


class UserEventUseCase(ABC):
    @abstractmethod
    async def log_event(self, body: UserEventCreate) -> UserEventRead:
        ...

    @abstractmethod
    async def list_by_user(
        self, user_id: int, event_type: str | None, limit: int
    ) -> list[UserEventRead]:
        ...
