from dataclasses import dataclass


@dataclass(frozen=True)
class CrewSmithCaptainEntity:
    id: int
    name: str
    memo: str
