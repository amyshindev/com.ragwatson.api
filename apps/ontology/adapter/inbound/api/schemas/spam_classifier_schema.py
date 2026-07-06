from pydantic import BaseModel, Field


class ClassifyEmailRequestSchema(BaseModel):
    sender: str | None = Field(None, description="발신자 (선택)")
    subject: str = Field(..., min_length=1, description="메일 제목")
    body: str = Field(..., min_length=1, description="메일 본문")

    model_config = {
        "json_schema_extra": {
            "example": {
                "sender": "noreply@suspicious.example",
                "subject": "URGENT: Verify your account NOW!!!",
                "body": "Click here to verify your account immediately.",
            }
        }
    }


class ClassifyEmailResponseSchema(BaseModel):
    label: str = Field(..., description="ham | spam | phishing | promo")
    score: float = Field(..., ge=0.0, le=1.0, description="위험 점수")
    is_blocked: bool = Field(..., description="발송 차단 여부")
    reasons: list[str] = Field(default_factory=list, description="판정 근거")
    matched_concepts: list[str] = Field(default_factory=list, description="온톨로지 개념 ID")
    source: str = Field(..., description="판정 소스 (repository 클래스명)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "label": "phishing",
                "score": 0.5,
                "is_blocked": True,
                "reasons": ["피싱: 계정·비밀번호 탈취 유도 (키워드: 'verify your account')"],
                "matched_concepts": ["concept:phishing_credential"],
                "source": "SpamOntologyMemoryRepository",
            }
        }
    }
