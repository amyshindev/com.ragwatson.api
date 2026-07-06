from dataclasses import dataclass


@dataclass(frozen=True)
class ClipEmbedderQuery:
    id: int
    name: str


@dataclass(frozen=True)
class ClipEmbedderResponse:
    id: int
    name: str
