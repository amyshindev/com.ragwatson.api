import logging

from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.dtos.walter_dto import WalterQuery
from titanic.adapter.inbound.api.schemas.walter_schema import WalterSchema
from titanic.app.ports.output.walter_repository import WalterRepository
from titanic.adapter.outbound.pg.walter_pg_repository import WalterPgRepository

log = logging.getLogger(__name__)


class WalterInteractor(WalterUseCase):

    def __init__(self):
        pass


    def introduce_myself(self, schema: WalterSchema):
        query = WalterQuery(
            id=schema.id, 
            name=schema.name,
            memo=schema.memo
        )
        log.info("########################################################")
        log.info("2️⃣  [WalterUseCase] router에서 가져온 월터 정보")
        log.info(f"2️⃣  ID: {query.id}")
        log.info(f"2️⃣  NAME: {query.name}")
        log.info(f"2️⃣  MEMO: {query.memo}")
        log.info("########################################################")

        walter: WalterRepository = WalterPgRepository()
        walter.introduce_myself(query)

        pass