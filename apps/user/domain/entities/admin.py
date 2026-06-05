from dataclasses import dataclass


@dataclass(frozen=True)
class Admin:
    """관리자 도메인 엔티티 — ADMINS 테이블 전용.

    일반 사용자(User)와 완전히 분리된 독립 엔티티.
    비밀번호는 저장소 경계(PgRepository)에서만 다룬다.
    """

    email: str
    username: str
    id: int | None = None
