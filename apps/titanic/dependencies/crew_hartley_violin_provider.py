from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from titanic.adapter.outbound.pg.crew_hartley_violin_pg_repository import CrewHartleyViolinPgRepository
from titanic.app.ports.input.crew_hartley_violin_use_case import CrewHartleyViolinUseCase
from titanic.app.ports.output.crew_hartley_violin_repository import CrewHartleyViolinRepository
from titanic.app.use_cases.crew_hartley_violin_interactor import CrewHartleyViolinInteractor


def get_crew_hartley_violin_use_case(
    db: AsyncSession = Depends(get_db),
) -> CrewHartleyViolinUseCase:
    repository: CrewHartleyViolinRepository = CrewHartleyViolinPgRepository(session=db)
    return CrewHartleyViolinInteractor(repository=repository)
