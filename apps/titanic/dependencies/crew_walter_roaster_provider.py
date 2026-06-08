from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from titanic.adapter.outbound.pg.crew_walter_roaster_pg_repository import CrewWalterRoasterPgRepository
from titanic.app.ports.input.crew_walter_roaster_use_case import CrewWalterRoasterUseCase
from titanic.app.ports.output.crew_walter_roaster_repository import CrewWalterRoasterRepository
from titanic.app.use_cases.crew_walter_roaster_interactor import CrewWalterRoasterInteractor


def get_crew_walter_roaster_use_case(
    db: AsyncSession = Depends(get_db),
) -> CrewWalterRoasterUseCase:
    repository: CrewWalterRoasterRepository = CrewWalterRoasterPgRepository(session=db)
    return CrewWalterRoasterInteractor(repository=repository)
