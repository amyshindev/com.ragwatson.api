import logging

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.walter_pg_repository import WalterPgRepository

log = logging.getLogger(__name__)


class WalterRepository:
    """Walter query 유스케이스에서 전달된 조회 요청을 받는 출력 포트."""

    def __init__(self, repository: WalterPgRepository | None = None) -> None:
        self._repository = repository or WalterPgRepository()

    async def get_dataframe_db(self, session: AsyncSession) -> pd.DataFrame:
        log.info("[WalterRepository] outbound 전달 — preview 조회")
        return await self._repository.get_dataframe_db(session)

