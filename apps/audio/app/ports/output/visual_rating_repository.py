from abc import ABC, abstractmethod
from uuid import UUID

from audio.adapter.inbound.api.schemas.visual_ratings import VisualRatingCreate
from audio.adapter.outbound.orm.visual_rating_orm import VisualRating


class VisualRatingRepository(ABC):
    @abstractmethod
    async def create(self, body: VisualRatingCreate) -> VisualRating:
        ...

    @abstractmethod
    async def list_by_generation(self, generation_id: UUID) -> list[VisualRating]:
        ...

    @abstractmethod
    async def get_avg_scores(self, generation_id: UUID) -> dict:
        ...

    @abstractmethod
    async def get_ab_test_result(self, ab_test_id: str) -> dict:
        ...

    @abstractmethod
    async def get_platform_avg(
        self, generation_id: UUID, platform: str | None
    ) -> dict:
        ...

    @abstractmethod
    async def flag_rating(
        self, rating_id: UUID, flag: str, reason: str | None
    ) -> VisualRating:
        ...
