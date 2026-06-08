from dataclasses import dataclass


@dataclass(frozen=True)
class CrewLoweBoatRole:
    slug: str = "crew_lowe_boat"
