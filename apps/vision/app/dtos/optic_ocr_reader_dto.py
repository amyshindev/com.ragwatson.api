from dataclasses import dataclass


@dataclass(frozen=True)
class OcrReaderQuery:
    id: int
    name: str


@dataclass(frozen=True)
class OcrReaderResponse:
    id: int
    name: str
