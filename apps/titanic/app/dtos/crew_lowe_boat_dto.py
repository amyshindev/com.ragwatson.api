from dataclasses import dataclass


@dataclass
class CrewLoweBoatQuery:
    id: int
    name: str


@dataclass
class CrewLoweBoatResponse:
    id: int
    name: str
