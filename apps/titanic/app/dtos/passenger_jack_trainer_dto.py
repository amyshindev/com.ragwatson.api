from dataclasses import dataclass


@dataclass
class PassengerJackTrainerQuery:
    id: int
    name: str


@dataclass
class PassengerJackTrainerResponse:
    id: int
    name: str
