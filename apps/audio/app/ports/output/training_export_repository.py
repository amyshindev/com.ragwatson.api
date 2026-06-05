from abc import ABC, abstractmethod

from ml_data.adapter.inbound.api.schemas.training_export import (
    DatasetStatsRead,
    TrainingRecord,
)


class TrainingExportRepository(ABC):
    @abstractmethod
    async def export_labeled_dataset(
        self,
        min_aesthetic_score: int = 3,
        limit: int = 10000,
    ) -> list[TrainingRecord]:
        ...

    @abstractmethod
    async def get_dataset_stats(self) -> DatasetStatsRead:
        ...
