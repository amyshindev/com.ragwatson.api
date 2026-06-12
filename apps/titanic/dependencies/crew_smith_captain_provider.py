from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.adapter.outbound.pg.crew_smith_captain_pg_repository import SmithCaptainPgRepository
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
from titanic.app.use_cases.crew_smith_captain_interactor import SmithCaptainInteractor
from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor
from titanic.app.use_cases.passenger_rose_model_interactor import RoseModelInteractor
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case
from titanic.dependencies.passenger_rose_model_provider import get_rose_model


def get_smith_captain_repository(
    db: AsyncSession = Depends(get_db),
) -> SmithCaptainRepository:
    return SmithCaptainPgRepository(session=db)


def get_smith_captain_use_case(
    repository: SmithCaptainRepository = Depends(get_smith_captain_repository),
    jack: JackTrainerInteractor = Depends(get_jack_trainer_use_case),
    rose: RoseModelInteractor = Depends(get_rose_model),
) -> SmithCaptainUseCase:
    return SmithCaptainInteractor(
        repository=repository,
        jack=jack,
        rose=rose,
    )
