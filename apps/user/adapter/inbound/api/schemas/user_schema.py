from typing import TYPE_CHECKING

from pydantic import BaseModel, EmailStr, Field

from user.domain.entities.user import User, UserRole

if TYPE_CHECKING:
    pass


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    nickname: str
    # role 제거 — v4: 관리자는 AdminResponse 로 분리

    model_config = {"from_attributes": True}

    @classmethod
    def from_entity(cls, user: User) -> "UserResponse":
        if user.id is None:
            raise ValueError("User id is required for API response")
        return cls(
            id=user.id,
            email=user.email,
            username=user.username,
            nickname=user.nickname,
        )


class UserSchema(BaseModel):
    """회원가입 요청 본문."""

    email: EmailStr = Field(..., description="이메일")
    username: str = Field(..., min_length=1, max_length=64, description="아이디")
    nickname: str = Field(..., min_length=1, max_length=64, description="닉네임")
    password: str = Field(..., min_length=1, max_length=128, description="비밀번호")
    # role 제거 — v4: 일반 회원가입은 항상 USER

    def to_entity(self) -> User:
        return User(
            email=str(self.email).strip().lower(),
            username=self.username.strip(),
            nickname=self.nickname.strip(),
        )


class SignupRequest(UserSchema):
    pass


class SignupResponse(BaseModel):
    ok: bool = True
    message: str = "회원가입이 완료되었습니다."
    user: UserResponse


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="이메일")
    password: str = Field(..., min_length=1, max_length=128, description="비밀번호")


class LoginResponse(BaseModel):
    ok: bool = True
    message: str = "로그인되었습니다."
    user: UserResponse
