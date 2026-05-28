from pydantic import BaseModel, EmailStr, Field

from secom.app.models.role import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=1, max_length=64)
    nickname: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=1, max_length=128)
    role: UserRole = UserRole.USER


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    nickname: str
    role: UserRole

    model_config = {"from_attributes": True}

