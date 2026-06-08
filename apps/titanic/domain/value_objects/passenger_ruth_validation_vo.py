from dataclasses import dataclass


@dataclass(frozen=True)
class PassengerRuthValidationRole:
    slug: str = "passenger_ruth_validation"
