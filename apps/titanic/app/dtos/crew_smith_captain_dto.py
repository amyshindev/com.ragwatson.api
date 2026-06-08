from dataclasses import dataclass


@dataclass
class CrewSmithCaptainQuery:
    id: int
    name: str


@dataclass
class CrewSmithCaptainResponse:
    id: int
    name: str
