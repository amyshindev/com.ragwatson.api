from pydantic import BaseModel, EmailStr, Field


class FakerEmailRequestSchema(BaseModel):
    to: EmailStr = Field(..., description="수신 이메일 주소")
    prompt: str = Field(..., min_length=1, description="메일 작성 지시")
    subject: str | None = Field(None, description="제목 (없으면 LLM이 생성)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "to": "recipient@example.com",
                "prompt": "타이타닉 automata 프로젝트 진행 상황을 정중하게 요약해줘",
                "subject": "[Automata] 프로젝트 요약",
            }
        }
    }


class FakerEmailResponseSchema(BaseModel):
    ok: bool = Field(..., description="발송 성공 여부")
    to: str = Field(..., description="수신 이메일")
    subject: str = Field(..., description="메일 제목")
    body_preview: str = Field(..., description="본문 미리보기 (앞 200자)")
    n8n_status: str = Field(..., description="n8n 응답 상태")

    model_config = {
        "json_schema_extra": {
            "example": {
                "ok": True,
                "to": "recipient@example.com",
                "subject": "[Automata] 프로젝트 요약",
                "body_preview": "안녕하세요,\n\n타이타닉 automata 프로젝트는…",
                "n8n_status": "sent",
            }
        }
    }
