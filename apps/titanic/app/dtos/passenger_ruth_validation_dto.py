from dataclasses import dataclass


@dataclass
class PassengerRuthValidationQuery:
    id: int
    name: str


@dataclass
class PassengerRuthValidationResponse:
    id: int
    name: str
