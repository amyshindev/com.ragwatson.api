from abc import ABC, abstractmethod
from uuid import UUID

from audio.adapter.inbound.api.schemas.visual_ratings import (
    AbTestResultRead,
    VisualRatingAvgRead,
    VisualRatingCreate,
    VisualRatingPlatformAvgRead,
    VisualRatingRead,
)


class VisualRatingUseCase(ABC):
    @abstractmethod
    async def submit_rating(self, body: VisualRatingCreate) -> VisualRatingRead:
        ...

    @abstractmethod
    async def get_ratings_by_generation(
        self, generation_id: UUID
    ) -> list[VisualRatingRead]:
        ...

    @abstractmethod
    async def get_avg_scores(self, generation_id: UUID) -> VisualRatingAvgRead:
        ...

    @abstractmethod
    async def get_ab_test_result(self, ab_test_id: str) -> AbTestResultRead:
        ...

    @abstractmethod
    async def get_platform_avg(
        self, generation_id: UUID, platform: str | None
    ) -> VisualRatingPlatformAvgRead:
        ...

    @abstractmethod
    async def flag_rating(
        self, rating_id: UUID, flag: str, reason: str | None
    ) -> VisualRatingRead:
        ...
