from pydantic import BaseModel, Field


class SmithCaptainSchema(BaseModel):
    id: int = Field(3, description="Captain ID")
    name: str = Field("에드워드 스미스", description="Captain's name")
    # 타이타닉호 선장 , 최종 항해를 지휘함

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Edward Smith",
            }
        }
    }


class ChatSchema(BaseModel):
    message: str = Field(..., min_length=1, description="사용자가 채팅창에 입력한 자연어 메시지")
    # POST /titanic/smith/chat 요청 본문

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "탑승객이 몇 명이야?",
            }
        }
    }


class ChatResponseSchema(BaseModel):
    reply: str = Field(..., description="선장의 답변")
    # POST /titanic/smith/chat 응답 본문

    model_config = {
        "json_schema_extra": {
            "example": {
                "reply": "오늘 항해는 맑은 날씨가 예상됩니다. 걱정 마십시오.",
            }
        }
    }
