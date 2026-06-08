from dataclasses import dataclass


@dataclass(frozen=True)
class CrewAndrewsArchitectEntity:
    id: int
    name: str
    memo: str
