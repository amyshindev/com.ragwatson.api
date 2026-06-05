from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from audio.adapter.outbound.pg.visual_rating_pg_repository import VisualRatingPgRepository
from audio.app.ports.input.visual_rating_use_case import VisualRatingUseCase
from audio.app.ports.output.visual_rating_repository import VisualRatingRepository
from audio.app.use_cases.visual_rating_interactor import VisualRatingInteractor


def get_visual_rating_use_case(
    db: AsyncSession = Depends(get_db),
) -> VisualRatingUseCase:
    repository: VisualRatingRepository = VisualRatingPgRepository(session=db)
    return VisualRatingInteractor(session=db, repository=repository)
