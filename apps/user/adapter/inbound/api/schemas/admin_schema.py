from pydantic import BaseModel, EmailStr, Field


class AdminSessionUser(BaseModel):
    id: int
    email: str
    username: str
    nickname: str
    role: str = "admin"


class AdminLoginRequest(BaseModel):
    email: EmailStr = Field(..., description="관리자 이메일")
    password: str = Field(..., min_length=1, max_length=128, description="비밀번호")


class AdminLoginResponse(BaseModel):
    ok: bool = True
    message: str = "관리자 로그인되었습니다."
    user: AdminSessionUser
