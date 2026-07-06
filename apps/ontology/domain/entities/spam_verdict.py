from __future__ import annotations

from dataclasses import dataclass, field

from ontology.domain.value_objects.spam_label import SpamLabel


@dataclass(frozen=True)
class SpamVerdict:
    label: SpamLabel
    score: float
    reasons: tuple[str, ...] = field(default_factory=tuple)
    matched_concepts: tuple[str, ...] = field(default_factory=tuple)

    @property
    def is_blocked(self) -> bool:
        return self.label.is_blocked
