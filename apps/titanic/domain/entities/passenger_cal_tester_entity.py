from dataclasses import dataclass


@dataclass(frozen=True)
class PassengerCalTesterEntity:
    id: int
    name: str
    memo: str
