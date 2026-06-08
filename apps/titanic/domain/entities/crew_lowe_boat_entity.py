from dataclasses import dataclass


@dataclass(frozen=True)
class CrewLoweBoatEntity:
    id: int
    name: str
    memo: str
