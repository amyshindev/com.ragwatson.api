from pydantic import BaseModel, EmailStr, Field

from secom.app.models.role import UserRole
from secom.app.models.schemas import UserCreate, UserResponse


class SignupRequest(BaseModel):
    """POST /signup 요청 본문."""

    email: EmailStr = Field(..., description="이메일")
    username: str = Field(..., min_length=1, max_length=64, description="아이디")
    nickname: str = Field(..., min_length=1, max_length=64, description="닉네임")
    password: str = Field(..., min_length=1, max_length=128, description="비밀번호")
    role: UserRole = Field(default=UserRole.USER, description="admin | user")

    def to_user_create(self) -> UserCreate:
        return UserCreate.model_validate(self.model_dump())


class SignupResponse(BaseModel):
    """POST /signup 응답."""

    ok: bool = True
    message: str = "회원가입이 완료되었습니다."
    user: UserResponse
