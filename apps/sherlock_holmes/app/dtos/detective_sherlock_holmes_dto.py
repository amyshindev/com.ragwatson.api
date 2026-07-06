from dataclasses import dataclass


@dataclass(frozen=True)
class SherlockHolmesQuery:
    id: int
    name: str


@dataclass(frozen=True)
class SherlockHolmesResponse:
    id: int
    name: str


DetectiveSherlockHolmesQuery = SherlockHolmesQuery
DetectiveSherlockHolmesResponse = SherlockHolmesResponse
