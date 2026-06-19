from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from siliconvalley.adapter.outbound.pg.bighetti_hr_repository import BighettiHrPgRepository
from siliconvalley.app.ports.input.bighetti_hr_use_case import BighettiHrUseCase
from siliconvalley.app.ports.output.bighetti_hr_port import BighettiHrPort
from siliconvalley.app.use_cases.bighetti_hr_interactor import BighettiHrInteractor


def get_bighetti_hr_repository(
    db: AsyncSession = Depends(get_db),
) -> BighettiHrPort:
    return BighettiHrPgRepository(session=db)


def get_bighetti_hr_use_case(
    repository: BighettiHrPort = Depends(get_bighetti_hr_repository),
) -> BighettiHrUseCase:
    return BighettiHrInteractor(repository=repository)
