from collections.abc import Sequence
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository

log = logging.getLogger(__name__)


class JamesRepository:
    """James command 유스케이스에서 전달된 업로드 데이터를 받는 출력 포트."""

    def __init__(self, repository: JamesPgRepository | None = None) -> None:
        self._repository = repository or JamesPgRepository()

    async def save_uploaded_rows(
        self,
        session: AsyncSession,
        filename: str,
        rows: Sequence[dict[str, str]],
    ) -> dict:
        log.info("[JamesRepository] outbound 전달 — filename=%s rows=%s", filename, len(rows))
        return await self._repository.save_uploaded_rows(session, filename, rows)
