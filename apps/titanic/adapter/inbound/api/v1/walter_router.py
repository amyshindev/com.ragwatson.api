import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.walter_schema import WalterSchema
from titanic.app.dtos.walter_dto import WalterResponse
from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.dependencies.walter import get_walter_use_case

log = logging.getLogger(__name__)

walter_router = APIRouter(prefix="/api/walter/v1", tags=["walter-reader"])


@walter_router.get("/myself")
async def introduce_myself(
    walter: WalterUseCase = Depends(get_walter_use_case),
) -> WalterResponse:
    schema = WalterSchema(
        id=2,
        name="Walter Kim",
        memo="타이타닉의 일등 항해사, 승객 명단 관리 담당.",
    )

    log.info("########################################################")
    log.info("1️⃣  [WalterRouter] schema에서 가져온 월터 자기소개글")
    log.info("1️⃣  ID: %s", schema.id)
    log.info("1️⃣  NAME: %s", schema.name)
    log.info("1️⃣  MEMO: %s", schema.memo)
    log.info("########################################################")

    await walter.introduce_myself(schema)

    return WalterResponse(
        id=schema.id,
        name=schema.name,
        memo=schema.memo,
    )
