from dataclasses import dataclass


@dataclass(frozen=True)
class PassengerRuthValidationEntity:
    id: int
    name: str
