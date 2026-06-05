from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from ml_data.adapter.outbound.pg.generation_log_pg_repository import GenerationLogPgRepository
from ml_data.app.ports.input.generation_log_use_case import GenerationLogUseCase
from ml_data.app.ports.output.generation_log_repository import GenerationLogRepository
from ml_data.app.use_cases.generation_log_interactor import GenerationLogInteractor


def get_generation_log_use_case(
    db: AsyncSession = Depends(get_db),
) -> GenerationLogUseCase:
    repository: GenerationLogRepository = GenerationLogPgRepository(session=db)
    return GenerationLogInteractor(session=db, repository=repository)
