from collections.abc import Sequence
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.use_cases.james_command import JamesCommandUseCase

log = logging.getLogger(__name__)


class JamesUseCase:
    """Inbound adapter에서 전달된 CSV 행 데이터를 받는 입력 포트 구현."""

    def __init__(self) -> None:
        self._command = JamesCommandUseCase()

    async def receive_uploaded_rows(
        self,
        session: AsyncSession,
        filename: str,
        rows: Sequence[dict[str, str]],
    ) -> dict:
        log.info("[JamesUseCase] 수신 완료 — filename=%s rows=%s", filename, len(rows))
        return await self._command.execute(session, filename, rows)
