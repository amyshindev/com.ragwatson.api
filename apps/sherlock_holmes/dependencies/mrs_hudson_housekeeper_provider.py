from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from sherlock_holmes.adapter.outbound.pg.mrs_hudson_housekeeper_repository import HudsonHousekeeperPgRepository
from sherlock_holmes.app.ports.input.mrs_hudson_housekeeper_use_case import HudsonHousekeeperUseCase
from sherlock_holmes.app.ports.output.mrs_hudson_housekeeper_port import HudsonHousekeeperPort
from sherlock_holmes.app.use_cases.mrs_hudson_housekeeper_interactor import HudsonHousekeeperInteractor


def get_mrs_hudson_housekeeper_repository(
    db: AsyncSession = Depends(get_db),
) -> HudsonHousekeeperPort:
    return HudsonHousekeeperPgRepository(session=db)


def get_mrs_hudson_housekeeper_use_case(
    repository: HudsonHousekeeperPort = Depends(get_mrs_hudson_housekeeper_repository),
) -> HudsonHousekeeperUseCase:
    return HudsonHousekeeperInteractor(repository=repository)
