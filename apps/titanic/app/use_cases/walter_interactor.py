import logging

from titanic.adapter.inbound.api.schemas.walter_schema import WalterSchema
from titanic.app.dtos.walter_dto import WalterQuery
from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.ports.output.walter_repository import WalterRepository

log = logging.getLogger(__name__)


class WalterInteractor(WalterUseCase):
    def __init__(self, repository: WalterRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: WalterSchema) -> None:
        query = WalterQuery(
            id=schema.id,
            name=schema.name,
            memo=schema.memo,
        )
        log.info("########################################################")
        log.info("2️⃣  [WalterUseCase] router에서 가져온 월터 정보")
        log.info("2️⃣  ID: %s", query.id)
        log.info("2️⃣  NAME: %s", query.name)
        log.info("2️⃣  MEMO: %s", query.memo)
        log.info("########################################################")

        await self._repository.introduce_myself(query)
