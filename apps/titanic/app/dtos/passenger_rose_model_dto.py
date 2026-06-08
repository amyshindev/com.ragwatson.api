from dataclasses import dataclass


@dataclass
class PassengerRoseModelQuery:
    id: int
    name: str


@dataclass
class PassengerRoseModelResponse:
    id: int
    name: str
