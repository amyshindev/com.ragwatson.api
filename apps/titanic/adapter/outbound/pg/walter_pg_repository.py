from titanic.app.ports.output.walter_repository import WalterRepository
from titanic.app.dtos.walter_dto import WalterQuery

import logging
log = logging.getLogger(__name__)


class WalterPgRepository(WalterRepository):

    def __init__(self):
        pass

    def introduce_myself(self, query: WalterQuery):
        log.info("########################################################")
        log.info("3️⃣  [WalterRepository] use_case에서 가져온 월터 정보")
        log.info(f"3️⃣  ID: {query.id}")
        log.info(f"3️⃣  NAME: {query.name}")
        log.info(f"3️⃣  MEMO: {query.memo}")
        log.info("########################################################")

        pass

