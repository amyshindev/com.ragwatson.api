from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from sherlock_holmes.adapter.outbound.pg.professor_moriarty_rival_repository import MoriartyRivalPgRepository
from sherlock_holmes.app.ports.input.professor_moriarty_rival_use_case import MoriartyRivalUseCase
from sherlock_holmes.app.ports.output.professor_moriarty_rival_port import MoriartyRivalPort
from sherlock_holmes.app.use_cases.professor_moriarty_rival_interactor import MoriartyRivalInteractor


def get_professor_moriarty_rival_repository(
    db: AsyncSession = Depends(get_db),
) -> MoriartyRivalPort:
    return MoriartyRivalPgRepository(session=db)


def get_professor_moriarty_rival_use_case(
    repository: MoriartyRivalPort = Depends(get_professor_moriarty_rival_repository),
) -> MoriartyRivalUseCase:
    return MoriartyRivalInteractor(repository=repository)
