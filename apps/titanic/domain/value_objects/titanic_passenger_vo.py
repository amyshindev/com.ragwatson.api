from dataclasses import dataclass


@dataclass(frozen=True)
class TitanicPassengerId:
    value: str
