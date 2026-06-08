from dataclasses import dataclass


@dataclass(frozen=True)
class CrewHartleyViolinEntity:
    id: int
    name: str
    memo: str
