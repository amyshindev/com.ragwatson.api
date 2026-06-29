from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class FordDirectorQuery:
    id: int
    name: str
    workflow: str = "default"
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FordDirectorResponse:
    id: int
    name: str
    role: str = "n8n workflow director"
    triggered: bool | None = None
    workflow: str | None = None
