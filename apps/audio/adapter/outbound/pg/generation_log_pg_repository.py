from datetime import datetime, timezone
import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from audio.adapter.inbound.api.schemas.generation_logs import GenerationLogCreate
from audio.adapter.outbound.orm.generation_log_orm import GenerationLog
from audio.app.ports.output.generation_log_repository import GenerationLogRepository

logger = logging.getLogger(__name__)

_RESULT_FIELDS = {
    "output_asset_url",
    "render_ms",
    "quality_score",
    "style_vector",
    "status",
    "error_message",
}
_LOOP_META_FIELDS = {
    "loop_duration_sec",
    "loop_beat_aligned",
    "frame_rate",
    "loop_sync_offset_ms",
    "target_platform",
    "aspect_ratio",
    "target_duration_sec",
}


class GenerationLogPgRepository(GenerationLogRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, body: GenerationLogCreate) -> GenerationLog:
        data = body.model_dump()
        user_id = data.pop("user_id")
        row = GenerationLog(user_id=user_id, status="pending", **data)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        logger.info(
            "[GenerationLogPgRepository] create id=%s status=%s",
            row.id,
            row.status,
        )
        return row

    async def get(self, generation_id: UUID) -> GenerationLog | None:
        result = await self._session.execute(
            select(GenerationLog).where(GenerationLog.id == generation_id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self,
        user_id: int,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[GenerationLog]:
        stmt = (
            select(GenerationLog)
            .where(GenerationLog.user_id == user_id)
            .order_by(GenerationLog.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        if status:
            stmt = stmt.where(GenerationLog.status == status)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def _update_fields(
        self, generation_id: UUID, payload: dict, allowed: set[str]
    ) -> GenerationLog:
        row = await self.get(generation_id)
        if row is None:
            raise ValueError(f"GenerationLog not found: {generation_id}")
        for key, value in payload.items():
            if key in allowed:
                setattr(row, key, value)
        if payload.get("status") == "completed":
            row.completed_at = datetime.now(timezone.utc)
        await self._session.flush()
        await self._session.refresh(row)
        return row

    async def update_result(self, generation_id: UUID, result: dict) -> GenerationLog:
        return await self._update_fields(generation_id, result, _RESULT_FIELDS)

    async def update_loop_meta(self, generation_id: UUID, meta: dict) -> GenerationLog:
        return await self._update_fields(generation_id, meta, _LOOP_META_FIELDS)
