import logging

from fastapi import APIRouter, HTTPException

from core.config import is_database_configured
from db.session import DbSession
from user.adapter.inbound.api.schemas import SignupRequest, SignupResponse
from user.adapter.outbound.pg.signup_pg_repository import SignupPgRepository
from user.app.use_cases.signup_interactor import SignupInteractor

log = logging.getLogger(__name__)

signup_router = APIRouter(prefix="/api/jason/v1", tags=["jason-signup"])


@signup_router.post("/signup", response_model=SignupResponse)
async def signup(req: SignupRequest, session: DbSession) -> SignupResponse:
    log.info("[SignupRouter] signup 요청 — email=%s", req.email)
    if not is_database_configured():
        raise HTTPException(status_code=503, detail="DATABASE_URL is not set.")

    try:
        use_case = SignupInteractor(session, SignupPgRepository(session))
        return await use_case.signup(req)
    except HTTPException:
        raise
    except Exception as exc:
        log.exception("signup failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
