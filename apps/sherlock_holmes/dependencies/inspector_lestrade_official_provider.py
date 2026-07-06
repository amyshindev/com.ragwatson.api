from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from sherlock_holmes.adapter.outbound.pg.inspector_lestrade_official_repository import LestradeOfficialPgRepository
from sherlock_holmes.app.ports.input.inspector_lestrade_official_use_case import LestradeOfficialUseCase
from sherlock_holmes.app.ports.output.inspector_lestrade_official_port import LestradeOfficialPort
from sherlock_holmes.app.use_cases.inspector_lestrade_official_interactor import LestradeOfficialInteractor


def get_inspector_lestrade_official_repository(
    db: AsyncSession = Depends(get_db),
) -> LestradeOfficialPort:
    return LestradeOfficialPgRepository(session=db)


def get_inspector_lestrade_official_use_case(
    repository: LestradeOfficialPort = Depends(get_inspector_lestrade_official_repository),
) -> LestradeOfficialUseCase:
    return LestradeOfficialInteractor(repository=repository)
