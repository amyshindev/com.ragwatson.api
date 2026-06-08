from dataclasses import dataclass


@dataclass
class PassengerIsidorCoupleQuery:
    id: int
    name: str


@dataclass
class PassengerIsidorCoupleResponse:
    id: int
    name: str
