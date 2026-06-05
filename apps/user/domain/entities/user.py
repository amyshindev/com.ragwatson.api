from dataclasses import dataclass
from enum import StrEnum


class UserRole(StrEnum):
    """Deprecated: v4에서 ADMINS 테이블로 분리됨.

    하위 호환을 위해 enum은 남겨두되,
    User 엔티티에서는 role 필드가 제거되었다.
    """

    ADMIN = "admin"
    USER = "user"


@dataclass(frozen=True)
class User:
    """회원 도메인 엔티티 (비밀번호는 저장소 경계에서만 다룸).

    v4: role 필드 제거 — 관리자는 Admin 엔티티(ADMINS 테이블)로 분리.
    """

    email: str
    username: str
    nickname: str
    id: int | None = None
