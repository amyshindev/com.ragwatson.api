from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from titanic.adapter.outbound.pg.crew_james_director_pg_repository import CrewJamesDirectorPgRepository
from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.crew_james_director_repository import JamesDirectorRepository
from titanic.app.use_cases.crew_james_director_interactor import JamesDirectorInteractor


def get_crew_james_director_use_case(
    db: AsyncSession = Depends(get_db),
) -> JamesDirectorUseCase:
    repository: JamesDirectorRepository = CrewJamesDirectorPgRepository(session=db)
    return JamesDirectorInteractor(repository=repository)
