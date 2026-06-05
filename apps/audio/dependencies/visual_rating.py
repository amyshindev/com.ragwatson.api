from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from ml_data.adapter.outbound.pg.visual_rating_pg_repository import VisualRatingPgRepository
from ml_data.app.ports.input.visual_rating_use_case import VisualRatingUseCase
from ml_data.app.ports.output.visual_rating_repository import VisualRatingRepository
from ml_data.app.use_cases.visual_rating_interactor import VisualRatingInteractor


def get_visual_rating_use_case(
    db: AsyncSession = Depends(get_db),
) -> VisualRatingUseCase:
    repository: VisualRatingRepository = VisualRatingPgRepository(session=db)
    return VisualRatingInteractor(session=db, repository=repository)
