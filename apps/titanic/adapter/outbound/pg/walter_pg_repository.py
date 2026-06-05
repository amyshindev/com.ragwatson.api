import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.walter_dto import WalterQuery
from titanic.app.ports.output.walter_repository import WalterRepository

log = logging.getLogger(__name__)


class WalterPgRepository(WalterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: WalterQuery) -> None:
        log.info("########################################################")
        log.info("3️⃣  [WalterRepository] use_case에서 가져온 월터 정보")
        log.info("3️⃣  ID: %s", query.id)
        log.info("3️⃣  NAME: %s", query.name)
        log.info("3️⃣  MEMO: %s", query.memo)
        log.info("########################################################")
