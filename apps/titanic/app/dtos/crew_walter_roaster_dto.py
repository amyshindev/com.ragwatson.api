from dataclasses import dataclass


@dataclass
class CrewWalterRoasterQuery:
    id: int
    name: str


@dataclass
class CrewWalterRoasterResponse:
    id: int
    name: str
