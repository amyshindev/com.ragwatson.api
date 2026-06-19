import logging

from fastapi import APIRouter, HTTPException

from core.config import is_database_configured
from db.session import DbSession
from user.adapter.inbound.api.schemas.admin_schema import AdminLoginRequest, AdminLoginResponse
from user.adapter.outbound.pg.admin_login_pg_repository import AdminLoginPgRepository
from user.app.use_cases.admin_login_interactor import AdminLoginInteractor

log = logging.getLogger(__name__)

admin_login_router = APIRouter(tags=["admin-login"])


@admin_login_router.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(req: AdminLoginRequest, session: DbSession) -> AdminLoginResponse:
    log.info("[AdminLoginRouter] admin login 요청 — email=%s", req.email)
    if not is_database_configured():
        raise HTTPException(status_code=503, detail="DATABASE_URL is not set.")

    try:
        use_case = AdminLoginInteractor(session, AdminLoginPgRepository(session))
        return await use_case.login(req)
    except HTTPException:
        raise
    except Exception as exc:
        log.exception("admin login failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
