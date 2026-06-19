from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from siliconvalley.adapter.outbound.pg.dinesh_dash_repository import DineshDashPgRepository
from siliconvalley.app.ports.input.dinesh_dash_use_case import DineshDashUseCase
from siliconvalley.app.ports.output.dinesh_dash_port import DineshDashPort
from siliconvalley.app.use_cases.dinesh_dash_interactor import DineshDashInteractor


def get_dinesh_dash_repository(
    db: AsyncSession = Depends(get_db),
) -> DineshDashPort:
    return DineshDashPgRepository(session=db)


def get_dinesh_dash_use_case(
    repository: DineshDashPort = Depends(get_dinesh_dash_repository),
) -> DineshDashUseCase:
    return DineshDashInteractor(repository=repository)
