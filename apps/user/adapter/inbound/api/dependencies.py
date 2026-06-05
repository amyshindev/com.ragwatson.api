"""Admin 인증 미들웨어 — admin_required 의존성.

v4: USERS.role 체크 → ADMINS 테이블 존재 여부 체크로 변경.

사용법:
    from user.adapter.inbound.api.dependencies import admin_required

    @router.get("/admin/something")
    async def admin_endpoint(admin: AdminRecord = Depends(admin_required)):
        ...
"""
from __future__ import annotations

import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import DbSession
from user.adapter.outbound.orm.admin_model import AdminRecord
from user.domain.entities.admin import Admin

log = logging.getLogger(__name__)

_bearer = HTTPBearer(auto_error=True)


def _bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> str:
    """Authorization: Bearer <token> 헤더에서 토큰을 추출한다."""
    return credentials.credentials


async def admin_required(
    token: str = Depends(_bearer_token),
    session: AsyncSession = Depends(DbSession),
) -> Admin:
    """관리자 전용 엔드포인트 의존성.

    JWT 토큰의 sub 값(admin_id)으로 ADMINS 테이블을 조회한다.
    레코드가 없거나 soft-delete 상태이면 403 반환.

    v4 변경:
        기존: users.role == 'admin' 검증
        신규: admins 테이블에 레코드 존재 여부 검증
    """
    from core.matrix.keymaker_api import keymaker

    try:
        payload = keymaker.verify_jwt(token)
    except Exception as exc:
        log.warning("admin_required: JWT 검증 실패 — %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    # JWT payload에서 sub_type 확인 — admin scope 토큰만 허용
    if payload.get("sub_type") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 전용 엔드포인트입니다.",
        )

    admin_id: int | None = payload.get("sub")
    if admin_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰에 식별자가 없습니다.",
        )

    result = await session.execute(
        select(AdminRecord).where(
            AdminRecord.id == int(admin_id),
            AdminRecord.deleted_at.is_(None),  # soft-delete 미적용 레코드만
        )
    )
    row = result.scalar_one_or_none()
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 계정이 존재하지 않거나 비활성 상태입니다.",
        )

    log.info("admin_required: 인증 완료 — admin_id=%s", row.id)
    return Admin(id=row.id, email=row.email, username=row.username)
