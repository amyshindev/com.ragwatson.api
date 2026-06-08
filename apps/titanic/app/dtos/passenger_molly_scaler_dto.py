from dataclasses import dataclass


@dataclass
class PassengerMollyScalerQuery:
    id: int
    name: str


@dataclass
class PassengerMollyScalerResponse:
    id: int
    name: str
