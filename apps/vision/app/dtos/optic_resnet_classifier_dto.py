from dataclasses import dataclass


@dataclass(frozen=True)
class ResnetClassifierQuery:
    id: int
    name: str


@dataclass(frozen=True)
class ResnetClassifierResponse:
    id: int
    name: str
