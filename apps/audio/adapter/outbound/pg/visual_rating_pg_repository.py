import logging
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from audio.adapter.inbound.api.schemas.visual_ratings import VisualRatingCreate
from audio.adapter.outbound.orm.visual_rating_orm import VisualRating
from audio.app.ports.output.visual_rating_repository import VisualRatingRepository

logger = logging.getLogger(__name__)


class VisualRatingPgRepository(VisualRatingRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, body: VisualRatingCreate) -> VisualRating:
        data = body.model_dump()
        rater_id = data.pop("rater_id")
        row = VisualRating(rater_id=rater_id, **data)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        logger.info(
            "[VisualRatingPgRepository] create id=%s gen=%s",
            row.id,
            row.generation_id,
        )
        return row

    async def list_by_generation(self, generation_id: UUID) -> list[VisualRating]:
        result = await self._session.execute(
            select(VisualRating)
            .where(VisualRating.generation_id == generation_id)
            .order_by(VisualRating.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_avg_scores(self, generation_id: UUID) -> dict:
        result = await self._session.execute(
            select(
                func.avg(VisualRating.aesthetic_score),
                func.avg(VisualRating.genre_match_score),
                func.avg(VisualRating.mood_match_score),
                func.count(VisualRating.id),
            ).where(VisualRating.generation_id == generation_id)
        )
        avg_aesthetic, avg_genre, avg_mood, total = result.one()
        return {
            "generation_id": generation_id,
            "avg_aesthetic": float(avg_aesthetic) if avg_aesthetic is not None else None,
            "avg_genre_match": float(avg_genre) if avg_genre is not None else None,
            "avg_mood_match": float(avg_mood) if avg_mood is not None else None,
            "total_count": int(total or 0),
        }

    async def get_ab_test_result(self, ab_test_id: str) -> dict:
        result = await self._session.execute(
            select(VisualRating).where(VisualRating.ab_test_id == ab_test_id)
        )
        rows = list(result.scalars().all())
        win_count = sum(1 for r in rows if r.ab_winner is True)
        lose_count = sum(1 for r in rows if r.ab_winner is False)
        winner_gen = next(
            (r.generation_id for r in rows if r.ab_winner is True),
            None,
        )
        return {
            "ab_test_id": ab_test_id,
            "winner_generation_id": winner_gen,
            "win_count": win_count,
            "lose_count": lose_count,
        }

    async def get_platform_avg(
        self, generation_id: UUID, platform: str | None
    ) -> dict:
        stmt = select(
            VisualRating.platform,
            func.avg(VisualRating.loop_smoothness_score),
            func.avg(VisualRating.beat_sync_score),
            func.count(VisualRating.id),
        ).where(VisualRating.generation_id == generation_id)
        if platform:
            stmt = stmt.where(VisualRating.platform == platform)
        stmt = stmt.group_by(VisualRating.platform)
        result = await self._session.execute(stmt)
        row = result.first()
        if row is None:
            return {
                "generation_id": generation_id,
                "platform": platform,
                "avg_loop_smoothness": None,
                "avg_beat_sync": None,
                "total_count": 0,
            }
        plat, avg_smooth, avg_sync, total = row
        return {
            "generation_id": generation_id,
            "platform": plat,
            "avg_loop_smoothness": float(avg_smooth) if avg_smooth is not None else None,
            "avg_beat_sync": float(avg_sync) if avg_sync is not None else None,
            "total_count": int(total or 0),
        }

    async def flag_rating(
        self, rating_id: UUID, flag: str, reason: str | None
    ) -> VisualRating:
        result = await self._session.execute(
            select(VisualRating).where(VisualRating.id == rating_id)
        )
        row = result.scalar_one_or_none()
        if row is None:
            raise ValueError(f"VisualRating not found: {rating_id}")
        row.flag = flag
        row.flag_reason = reason
        await self._session.flush()
        await self._session.refresh(row)
        return row
