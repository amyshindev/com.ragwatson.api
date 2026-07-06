from dataclasses import dataclass


@dataclass(frozen=True)
class MoriartyRivalQuery:
    id: int
    name: str


@dataclass(frozen=True)
class MoriartyRivalResponse:
    id: int
    name: str


ProfessorMoriartyRivalQuery = MoriartyRivalQuery
ProfessorMoriartyRivalResponse = MoriartyRivalResponse
