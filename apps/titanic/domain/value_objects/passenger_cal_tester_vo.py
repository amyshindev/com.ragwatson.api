from dataclasses import dataclass


@dataclass(frozen=True)
class PassengerCalTesterRole:
    slug: str = "passenger_cal_tester"
