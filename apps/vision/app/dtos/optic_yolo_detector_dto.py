from dataclasses import dataclass


@dataclass(frozen=True)
class YoloDetectorQuery:
    id: int
    name: str


@dataclass(frozen=True)
class YoloDetectorResponse:
    id: int
    name: str
