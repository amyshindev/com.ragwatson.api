from dataclasses import dataclass


@dataclass(frozen=True)
class PassengerJackTrainerEntity:
    id: int
    name: str
    memo: str
