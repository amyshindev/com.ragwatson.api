from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from titanic.adapter.outbound.pg.crew_smith_captain_repository import SmithCaptainPgRepository
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort
from titanic.app.use_cases.crew_andrews_architect_interactor import AndrewsArchitectInteractor
from titanic.app.use_cases.crew_hartley_violin_interactor import HartleyViolinInteractor
from titanic.app.use_cases.crew_smith_captain_interactor import SmithCaptainInteractor
from titanic.app.use_cases.crew_walter_roaster_interactor import WalterRoasterInteractor
from titanic.app.use_cases.passenger_cal_tester_interactor import CalTesterInteractor
from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainerInteractor
from titanic.app.use_cases.passenger_rose_model_interactor import RoseModelInteractor
from titanic.dependencies.crew_andrews_architect_provider import get_andrews_architect_use_case
from titanic.dependencies.crew_hartley_violin_provider import (
    get_hartley_violin_correlation_use_case,
)
from titanic.dependencies.crew_walter_roaster_provider import get_walter_roaster_use_case
from titanic.dependencies.passenger_cal_tester_provider import get_cal_tester_use_case
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case
from titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case


def get_smith_captain_repository(
    db: AsyncSession = Depends(get_db),
) -> SmithCaptainPort:
    return SmithCaptainPgRepository(session=db)


def get_smith_captain_use_case(
    repository: SmithCaptainPort = Depends(get_smith_captain_repository),
    andrews: AndrewsArchitectInteractor = Depends(get_andrews_architect_use_case),
    jack: JackTrainerInteractor = Depends(get_jack_trainer_use_case),
    rose: RoseModelInteractor = Depends(get_rose_model_use_case),
    cal: CalTesterInteractor = Depends(get_cal_tester_use_case),
    walter: WalterRoasterInteractor = Depends(get_walter_roaster_use_case),
    hartley: HartleyViolinInteractor = Depends(get_hartley_violin_correlation_use_case),
) -> SmithCaptainUseCase:

    return SmithCaptainInteractor(
        repository=repository,
        andrews=andrews,
        jack=jack,
        rose=rose,
        cal=cal,
        walter=walter,
        hartley=hartley,
    )
