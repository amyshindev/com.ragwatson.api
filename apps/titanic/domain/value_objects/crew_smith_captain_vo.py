from dataclasses import dataclass


@dataclass(frozen=True)
class CrewSmithCaptainRole:
    slug: str = "crew_smith_captain"
