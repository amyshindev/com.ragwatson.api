from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from ml_data.adapter.outbound.pg.training_export_pg_repository import (
    TrainingExportPgRepository,
)
from ml_data.app.ports.input.training_export_use_case import TrainingExportUseCase
from ml_data.app.ports.output.training_export_repository import TrainingExportRepository
from ml_data.app.use_cases.training_export_interactor import TrainingExportInteractor


def get_training_export_use_case(
    db: AsyncSession = Depends(get_db),
) -> TrainingExportUseCase:
    repository: TrainingExportRepository = TrainingExportPgRepository(session=db)
    return TrainingExportInteractor(session=db, repository=repository)
