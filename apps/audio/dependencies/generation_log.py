from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from audio.adapter.outbound.pg.generation_log_pg_repository import GenerationLogPgRepository
from audio.app.ports.input.generation_log_use_case import GenerationLogUseCase
from audio.app.ports.output.generation_log_repository import GenerationLogRepository
from audio.app.use_cases.generation_log_interactor import GenerationLogInteractor
from core.matrix.oracle_database import get_db


def get_generation_log_use_case(
    db: AsyncSession = Depends(get_db),
) -> GenerationLogUseCase:
    repository: GenerationLogRepository = GenerationLogPgRepository(session=db)
    return GenerationLogInteractor(session=db, repository=repository)
