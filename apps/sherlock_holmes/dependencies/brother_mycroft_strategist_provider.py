from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from sherlock_holmes.adapter.outbound.pg.brother_mycroft_strategist_repository import MycroftStrategistPgRepository
from sherlock_holmes.app.ports.input.brother_mycroft_strategist_use_case import MycroftStrategistUseCase
from sherlock_holmes.app.ports.output.brother_mycroft_strategist_port import MycroftStrategistPort
from sherlock_holmes.app.use_cases.brother_mycroft_strategist_interactor import MycroftStrategistInteractor


def get_brother_mycroft_strategist_repository(
    db: AsyncSession = Depends(get_db),
) -> MycroftStrategistPort:
    return MycroftStrategistPgRepository(session=db)


def get_brother_mycroft_strategist_use_case(
    repository: MycroftStrategistPort = Depends(get_brother_mycroft_strategist_repository),
) -> MycroftStrategistUseCase:
    return MycroftStrategistInteractor(repository=repository)
