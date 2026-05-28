import logging

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.use_cases.walter_query import WalterQueryUseCase

log = logging.getLogger(__name__)


class WalterUseCase:
    """Inbound adapter에서 전달된 preview 조회 요청을 받는 입력 포트 구현."""

    def __init__(self) -> None:
        self._query = WalterQueryUseCase()

    async def preview_uploaded_rows(self, session: AsyncSession) -> pd.DataFrame:
        log.info("[WalterUseCase] 수신 완료 — preview 조회 요청")
        return await self._query.execute(session)

