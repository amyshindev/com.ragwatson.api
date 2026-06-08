from dataclasses import dataclass


@dataclass(frozen=True)
class PassengerRoseModelRole:
    slug: str = "passenger_rose_model"
