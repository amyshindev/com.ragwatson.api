from dataclasses import dataclass


@dataclass(frozen=True)
class WatsonChroniclerQuery:
    id: int
    name: str


@dataclass(frozen=True)
class WatsonChroniclerResponse:
    id: int
    name: str


DoctorWatsonChroniclerQuery = WatsonChroniclerQuery
DoctorWatsonChroniclerResponse = WatsonChroniclerResponse
