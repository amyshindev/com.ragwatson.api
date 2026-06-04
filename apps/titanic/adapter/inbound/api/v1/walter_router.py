import logging

from fastapi import APIRouter
from titanic.adapter.inbound.api.schemas.walter_schema import WalterSchema
from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.use_cases.walter_interactor import WalterInteractor

log = logging.getLogger(__name__)

walter_router = APIRouter(prefix="/api/walter/v1", tags=["walter-reader"])


@walter_router.get("/myself")
async def introduce_myself():
    schema = WalterSchema()

    log.info("########################################################")
    log.info("1️⃣  [WalterRouter] schema에서 가져온 월터 자기소개글")
    log.info(f"1️⃣  ID: {schema.id}")
    log.info(f"1️⃣  NAME: {schema.name}")
    log.info(f"1️⃣  MEMO: {schema.memo}")
    log.info("########################################################")


    walter: WalterUseCase = WalterInteractor()
    walter.introduce_myself(schema)

    return {"id": schema.id, "name": schema.name, "memo": schema.memo}