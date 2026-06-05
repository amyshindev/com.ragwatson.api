from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from ml_data.adapter.inbound.api.schemas.training_export import (
    DatasetStatsRead,
    TrainingRecord,
)
from ml_data.app.ports.input.training_export_use_case import TrainingExportUseCase
from ml_data.app.ports.output.training_export_repository import TrainingExportRepository

log = logging.getLogger(__name__)


class TrainingExportInteractor(TrainingExportUseCase):
    def __init__(
        self,
        session: AsyncSession,
        repository: TrainingExportRepository,
    ) -> None:
        self._session = session
        self._repository = repository

    async def export_labeled_dataset(
        self,
        min_aesthetic_score: int = 3,
        limit: int = 10000,
        format: str = "jsonl",
    ) -> list[TrainingRecord]:
        if format not in {"jsonl", "csv"}:
            raise ValueError(f"Unsupported format: {format}")
        records = await self._repository.export_labeled_dataset(
            min_aesthetic_score, limit
        )
        log.info("[TrainingExportInteractor] export count=%s format=%s", len(records), format)
        return records

    async def get_dataset_stats(self) -> DatasetStatsRead:
        return await self._repository.get_dataset_stats()
