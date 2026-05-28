import logging

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.walter_repository import WalterRepository

log = logging.getLogger(__name__)


class WalterQueryUseCase:
    """walter input port에서 전달된 preview 조회를 처리하는 유스케이스."""

    def __init__(self, repository: WalterRepository | None = None) -> None:
        self._repository = repository or WalterRepository()

    async def execute(self, session: AsyncSession) -> pd.DataFrame:
        log.info("[WalterQueryUseCase] execute 시작 — preview 조회")
        return await self._repository.get_dataframe_db(session)

