import logging

from fastapi import APIRouter, HTTPException

from db.session import DbSession
from titanic.adapter.inbound.schemas.titanic_request import TitanicPassengerCreateRequest
from titanic.adapter.inbound.schemas.titanic_response import TitanicPassengerCreateResponse
from titanic.app.use_cases.titanic_command_impl import TitanicCommandUseCase

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/titanic/v1", tags=["titanic-command"])
_use_case = TitanicCommandUseCase()


@router.post("/passengers", response_model=TitanicPassengerCreateResponse)
async def create_passenger(
    body: TitanicPassengerCreateRequest,
    session: DbSession,
) -> TitanicPassengerCreateResponse:
    try:
        db_id, passenger = await _use_case.create_passenger(session, body.to_entity())
        await session.commit()
        return TitanicPassengerCreateResponse.from_entity(db_id, passenger)
    except HTTPException:
        await session.rollback()
        raise
    except Exception as exc:
        await session.rollback()
        log.exception("titanic command create_passenger failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
