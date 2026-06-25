from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from siliconvalley.adapter.outbound.pg.gilfoyle_system_repository import GilfoyleSystemPgRepository
from siliconvalley.app.ports.input.gilfoyle_system_use_case import GilfoyleSystemUseCase
from siliconvalley.app.ports.output.gilfoyle_system_port import GilfoyleSystemPort
from siliconvalley.app.use_cases.gilfoyle_system_interactor import GilfoyleSystemInteractor

from core.matrix.grid_oracle_database_manager import get_db


def get_gilfoyle_system_repository(
    db: AsyncSession = Depends(get_db),
) -> GilfoyleSystemPort:
    return GilfoyleSystemPgRepository(session=db)


def get_gilfoyle_system_use_case(
    repository: GilfoyleSystemPort = Depends(get_gilfoyle_system_repository),
) -> GilfoyleSystemUseCase:
    return GilfoyleSystemInteractor(repository=repository)
