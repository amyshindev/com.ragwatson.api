from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from titanic.adapter.outbound.pg.crew_andrews_architect_pg_repository import CrewAndrewsArchitectPgRepository
from titanic.app.ports.input.crew_andrews_architect_use_case import CrewAndrewsArchitectUseCase
from titanic.app.ports.output.crew_andrews_architect_repository import CrewAndrewsArchitectRepository
from titanic.app.use_cases.crew_andrews_architect_interactor import CrewAndrewsArchitectInteractor


def get_crew_andrews_architect_use_case(
    db: AsyncSession = Depends(get_db),
) -> CrewAndrewsArchitectUseCase:
    repository: CrewAndrewsArchitectRepository = CrewAndrewsArchitectPgRepository(session=db)
    return CrewAndrewsArchitectInteractor(repository=repository)
