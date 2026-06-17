from dataclasses import dataclass, field

from pydantic import BaseModel


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class SmithCaptainQuery:
    
    id: int   # 직관적인 타입 변경
    name: str

@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class SmithCaptainResponse:
    
    id: int   # 직관적인 타입 변경
    name: str


@dataclass(frozen=True)
class SmithCaptainChatQuery:
    message: str


class ChatResponse(BaseModel):
    reply: str
    accuracy: float | None = None


CrewSmithCaptainQuery = SmithCaptainQuery
CrewSmithCaptainResponse = SmithCaptainResponse
CrewSmithCaptainChatQuery = SmithCaptainChatQuery
