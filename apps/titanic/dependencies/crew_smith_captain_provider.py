from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from titanic.adapter.outbound.pg.crew_smith_captain_pg_repository import CrewSmithCaptainPgRepository
from titanic.app.ports.input.crew_smith_captain_use_case import CrewSmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_repository import CrewSmithCaptainRepository
from titanic.app.use_cases.crew_smith_captain_interactor import CrewSmithCaptainInteractor


def get_crew_smith_captain_use_case(
    db: AsyncSession = Depends(get_db),
) -> CrewSmithCaptainUseCase:
    repository: CrewSmithCaptainRepository = CrewSmithCaptainPgRepository(session=db)
    return CrewSmithCaptainInteractor(repository=repository)
