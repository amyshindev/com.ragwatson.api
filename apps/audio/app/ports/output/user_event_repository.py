from abc import ABC, abstractmethod

from ml_data.adapter.inbound.api.schemas.user_events import UserEventCreate
from ml_data.adapter.outbound.orm.user_event_orm import UserEvent


class UserEventRepository(ABC):
    @abstractmethod
    async def create(self, body: UserEventCreate) -> UserEvent:
        ...

    @abstractmethod
    async def list_by_user(
        self,
        user_id: int,
        event_type: str | None = None,
        limit: int = 50,
    ) -> list[UserEvent]:
        ...
