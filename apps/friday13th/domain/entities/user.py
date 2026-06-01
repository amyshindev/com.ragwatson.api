from dataclasses import dataclass
from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"


@dataclass(frozen=True)
class User:
    """회원 도메인 엔티티 (비밀번호는 저장소 경계에서만 다룸)."""

    email: str
    username: str
    nickname: str
    role: UserRole
    id: int | None = None
