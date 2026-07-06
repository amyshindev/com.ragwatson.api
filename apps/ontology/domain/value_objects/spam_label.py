from __future__ import annotations

from enum import StrEnum


class SpamLabel(StrEnum):
    HAM = "ham"
    SPAM = "spam"
    PHISHING = "phishing"
    PROMO = "promo"

    @property
    def is_blocked(self) -> bool:
        return self is not SpamLabel.HAM
