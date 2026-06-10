from dataclasses import dataclass


@dataclass
class TitanicPassenger:
    """CSV/API용 타이타닉 승객 플랫 엔티티."""

    passenger_id: int
    survived: int | str
    pclass: int | str
    name: str
    gender: str
    age: float | str | None
    sibsp: int | str
    parch: int | str
    ticket: str
    fare: float | str
    cabin: str
    embarked: str
