from dataclasses import dataclass


@dataclass(frozen=True)
class PassengerIsidorCoupleEntity:
    id: int
    name: str
    memo: str
