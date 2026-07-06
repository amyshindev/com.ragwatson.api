from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClassifyEmailCommand:
    sender: str | None
    subject: str
    body: str


@dataclass(frozen=True)
class ClassifyEmailResult:
    label: str
    score: float
    is_blocked: bool
    reasons: tuple[str, ...]
    matched_concepts: tuple[str, ...]
    source: str
