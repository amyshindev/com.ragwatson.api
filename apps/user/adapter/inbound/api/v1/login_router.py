import logging

from fastapi import APIRouter, HTTPException

from core.config import is_database_configured
from db.session import DbSession
from user.adapter.inbound.api.schemas import LoginRequest, LoginResponse
from user.adapter.outbound.pg.login_pg_repository import LoginPgRepository
from user.app.use_cases.login_interactor import LoginInteractor

log = logging.getLogger(__name__)

login_router = APIRouter(prefix="/api/jason/v1", tags=["jason-login"])


@login_router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, session: DbSession) -> LoginResponse:
    log.info("[LoginRouter] login 요청 — email=%s", req.email)
    if not is_database_configured():
        raise HTTPException(status_code=503, detail="DATABASE_URL is not set.")

    try:
        use_case = LoginInteractor(session, LoginPgRepository(session))
        return await use_case.login(req)
    except HTTPException:
        raise
    except Exception as exc:
        log.exception("login failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
