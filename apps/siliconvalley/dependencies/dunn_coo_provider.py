from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from siliconvalley.adapter.outbound.pg.dunn_coo_repository import DunnCooPgRepository
from siliconvalley.app.ports.input.dunn_coo_use_case import DunnCooUseCase
from siliconvalley.app.ports.output.dunn_coo_port import DunnCooPort
from siliconvalley.app.use_cases.dunn_coo_interactor import DunnCooInteractor

from core.matrix.grid_oracle_database_manager import get_db


def get_dunn_coo_repository(
    db: AsyncSession = Depends(get_db),
) -> DunnCooPort:
    return DunnCooPgRepository(session=db)


def get_dunn_coo_use_case(
    repository: DunnCooPort = Depends(get_dunn_coo_repository),
) -> DunnCooUseCase:
    return DunnCooInteractor(repository=repository)
