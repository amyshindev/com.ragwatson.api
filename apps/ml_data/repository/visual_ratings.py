import logging

from sqlalchemy.ext.asyncio import AsyncSession

from ml_data.models.visual_ratings import VisualRating
from ml_data.schemas.visual_ratings import VisualRatingCreate

logger = logging.getLogger(__name__)


class VisualRatingRepository:
    async def create(
        self, session: AsyncSession, body: VisualRatingCreate
    ) -> VisualRating:
        data = body.model_dump()
        rater_id = data.pop("rater_id")
        row = VisualRating(rater_id=rater_id, **data)
        session.add(row)
        await session.flush()
        await session.refresh(row)
        logger.info("[VisualRatingRepository] create id=%s gen=%s", row.id, row.generation_id)
        return row
