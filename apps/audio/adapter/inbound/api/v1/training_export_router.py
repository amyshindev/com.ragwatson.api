from fastapi import APIRouter, Depends, HTTPException, Query

from audio.adapter.inbound.api.schemas.training_export import (
    DatasetStatsRead,
    TrainingRecord,
)
from audio.app.ports.input.training_export_use_case import TrainingExportUseCase
from audio.dependencies.training_export import get_training_export_use_case

training_export_router = APIRouter(prefix="/api/ml", tags=["ml-data-export"])


@training_export_router.get("/export/training-set", response_model=list[TrainingRecord])
async def export_training_set(
    min_aesthetic_score: int = Query(default=3, ge=1, le=5),
    limit: int = Query(default=10000, ge=1, le=50000),
    format: str = Query(default="jsonl"),
    use_case: TrainingExportUseCase = Depends(get_training_export_use_case),
) -> list[TrainingRecord]:
    try:
        return await use_case.export_labeled_dataset(
            min_aesthetic_score, limit, format
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@training_export_router.get("/export/stats", response_model=DatasetStatsRead)
async def get_dataset_stats(
    use_case: TrainingExportUseCase = Depends(get_training_export_use_case),
) -> DatasetStatsRead:
    return await use_case.get_dataset_stats()
