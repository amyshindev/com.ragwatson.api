"""도메인 폼 데이터 영속화 (SQLAlchemy)."""

import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from domain_intake.models.domain_intake_record import DomainIntakeRecord

logger = logging.getLogger(__name__)


class DomainIntakeRepository:
    async def append(
        self,
        session: AsyncSession,
        kind: str,
        payload: dict[str, Any],
    ) -> int:
        row = DomainIntakeRecord(kind=kind, payload=payload)
        session.add(row)
        await session.flush()
        logger.info(
            "[DomainIntakeRepository] append kind=%s id=%s payload_keys=%s",
            kind,
            row.id,
            sorted(payload.keys()),
        )
        assert row.id is not None
        return row.id
