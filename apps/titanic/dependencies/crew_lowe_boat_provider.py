from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from titanic.adapter.outbound.pg.crew_lowe_boat_pg_repository import CrewLoweBoatPgRepository
from titanic.app.ports.input.crew_lowe_boat_use_case import CrewLoweBoatUseCase
from titanic.app.ports.output.crew_lowe_boat_repository import CrewLoweBoatRepository
from titanic.app.use_cases.crew_lowe_boat_interactor import CrewLoweBoatInteractor


def get_crew_lowe_boat_use_case(
    db: AsyncSession = Depends(get_db),
) -> CrewLoweBoatUseCase:
    repository: CrewLoweBoatRepository = CrewLoweBoatPgRepository(session=db)
    return CrewLoweBoatInteractor(repository=repository)
