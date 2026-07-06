from dataclasses import dataclass


@dataclass(frozen=True)
class LestradeOfficialQuery:
    id: int
    name: str


@dataclass(frozen=True)
class LestradeOfficialResponse:
    id: int
    name: str


InspectorLestradeOfficialQuery = LestradeOfficialQuery
InspectorLestradeOfficialResponse = LestradeOfficialResponse
