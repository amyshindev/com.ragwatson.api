from dataclasses import dataclass


@dataclass(frozen=True)
class MycroftStrategistQuery:
    id: int
    name: str


@dataclass(frozen=True)
class MycroftStrategistResponse:
    id: int
    name: str


BrotherMycroftStrategistQuery = MycroftStrategistQuery
BrotherMycroftStrategistResponse = MycroftStrategistResponse
