from dataclasses import dataclass


@dataclass
class PassengerCalTesterQuery:
    id: int
    name: str


@dataclass
class PassengerCalTesterResponse:
    id: int
    name: str
