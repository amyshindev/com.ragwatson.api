from dataclasses import dataclass


@dataclass(frozen=True)
class PassengerRoseModelEntity:
    id: int
    name: str
    memo: str
