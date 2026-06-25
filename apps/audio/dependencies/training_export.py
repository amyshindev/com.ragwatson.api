from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from audio.adapter.outbound.pg.training_export_pg_repository import (
    TrainingExportPgRepository,
)
from audio.app.ports.input.training_export_use_case import TrainingExportUseCase
from audio.app.ports.output.training_export_repository import TrainingExportRepository
from audio.app.use_cases.training_export_interactor import TrainingExportInteractor
from core.matrix.oracle_database import get_db


def get_training_export_use_case(
    db: AsyncSession = Depends(get_db),
) -> TrainingExportUseCase:
    repository: TrainingExportRepository = TrainingExportPgRepository(session=db)
    return TrainingExportInteractor(session=db, repository=repository)
