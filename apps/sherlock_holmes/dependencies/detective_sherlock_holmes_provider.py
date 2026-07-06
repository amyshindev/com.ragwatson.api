from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from sherlock_holmes.adapter.outbound.pg.detective_sherlock_holmes_repository import SherlockHolmesPgRepository
from sherlock_holmes.app.ports.input.detective_sherlock_holmes_use_case import SherlockHolmesUseCase
from sherlock_holmes.app.ports.output.detective_sherlock_holmes_port import SherlockHolmesPort
from sherlock_holmes.app.use_cases.detective_sherlock_holmes_interactor import SherlockHolmesInteractor


def get_detective_sherlock_holmes_repository(
    db: AsyncSession = Depends(get_db),
) -> SherlockHolmesPort:
    return SherlockHolmesPgRepository(session=db)


def get_detective_sherlock_holmes_use_case(
    repository: SherlockHolmesPort = Depends(get_detective_sherlock_holmes_repository),
) -> SherlockHolmesUseCase:
    return SherlockHolmesInteractor(repository=repository)
