from collections.abc import Sequence
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.james_repository import JamesRepository

log = logging.getLogger(__name__)


class JamesCommandUseCase:
    """james input port에서 전달된 업로드 행 데이터를 처리하는 유스케이스."""

    def __init__(self, repository: JamesRepository | None = None) -> None:
        self._repository = repository or JamesRepository()

    async def execute(
        self,
        session: AsyncSession,
        filename: str,
        rows: Sequence[dict[str, str]],
    ) -> dict:
        log.info("[JamesCommandUseCase] execute 시작 — filename=%s rows=%s", filename, len(rows))
        return await self._repository.save_uploaded_rows(session, filename, rows)
