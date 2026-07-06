from dataclasses import dataclass


@dataclass(frozen=True)
class SamSegmenterQuery:
    id: int
    name: str


@dataclass(frozen=True)
class SamSegmenterResponse:
    id: int
    name: str
