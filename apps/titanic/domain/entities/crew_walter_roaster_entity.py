from dataclasses import dataclass


@dataclass(frozen=True)
class CrewWalterRoasterEntity:
    id: int
    name: str
    memo: str
