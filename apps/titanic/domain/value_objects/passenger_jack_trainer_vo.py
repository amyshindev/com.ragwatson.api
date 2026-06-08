from dataclasses import dataclass


@dataclass(frozen=True)
class PassengerJackTrainerRole:
    slug: str = "passenger_jack_trainer"
