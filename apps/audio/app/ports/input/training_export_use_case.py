from abc import ABC, abstractmethod

from audio.adapter.inbound.api.schemas.training_export import (
    DatasetStatsRead,
    TrainingRecord,
)


class TrainingExportUseCase(ABC):
    @abstractmethod
    async def export_labeled_dataset(
        self,
        min_aesthetic_score: int = 3,
        limit: int = 10000,
        format: str = "jsonl",
    ) -> list[TrainingRecord]:
        ...

    @abstractmethod
    async def get_dataset_stats(self) -> DatasetStatsRead:
        ...
