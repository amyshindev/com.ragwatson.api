import logging

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.use_cases.reader_use_case import WalterReader

log = logging.getLogger(__name__)


class TitanicReader:
    def __init__(self, session: AsyncSession | None = None) -> None:
        self._reader = WalterReader(session)

    async def get_dataframe_db(self) -> pd.DataFrame:
        log.info("[TitanicReaderPort] use_case 호출 — get_dataframe_db")
        return await self._reader.get_dataframe_db()


__all__ = ["TitanicReader"]
