from pydantic import BaseModel, Field


class ContactUploadRowSchema(BaseModel):
    nickname: str | None = Field(None, description="닉네임 또는 이름")
    email: str | None = Field(None, description="이메일 주소")


class ContactItemSchema(BaseModel):
    id: int
    nickname: str
    email: str


class ContactListResponseSchema(BaseModel):
    items: list[ContactItemSchema]
    total: int
    page: int
    page_size: int
