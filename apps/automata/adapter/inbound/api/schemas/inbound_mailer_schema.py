from __future__ import annotations

import re

from pydantic import BaseModel, Field, field_validator


class InboundMailReceiveSchema(BaseModel):
    message_id: str | None = Field(None, description="Gmail message id")
    from_email: str = Field(..., alias="from", description="발신 이메일")
    from_name: str | None = Field(None, description="발신자 이름")
    subject: str = Field(default="", description="제목")
    body: str = Field(default="", description="본문")

    model_config = {"populate_by_name": True}

    @field_validator("from_email", mode="before")
    @classmethod
    def normalize_from(cls, value: object) -> str:
        text = str(value or "").strip()
        if not text:
            raise ValueError("from is required")

        name_match = re.match(r"^(?P<name>.*?)<(?P<email>[^>]+)>$", text)
        if name_match:
            return name_match.group("email").strip()

        email_match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", text)
        if email_match:
            return email_match.group(0).lower()

        return text.lower()


class InboundMailReceiveResponseSchema(BaseModel):
    ok: bool
    id: int
    duplicate: bool = False


class InboundMailItemSchema(BaseModel):
    id: int
    message_id: str
    from_email: str
    from_name: str | None
    subject: str
    body: str
    received_at: str


class InboundMailListResponseSchema(BaseModel):
    items: list[InboundMailItemSchema]
    total: int
    page: int
    page_size: int
