from dataclasses import dataclass


@dataclass(frozen=True)
class PassengerMollyScalerEntity:
    id: int
    name: str
    memo: str
