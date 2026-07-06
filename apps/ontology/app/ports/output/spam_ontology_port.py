from __future__ import annotations

from abc import ABC, abstractmethod

from ontology.domain.entities.email_signal import EmailSignal
from ontology.domain.entities.spam_verdict import SpamVerdict


class SpamOntologyPort(ABC):
    @abstractmethod
    async def enrich_verdict(self, signal: EmailSignal, base: SpamVerdict) -> SpamVerdict:
        """Merge graph-backed concept matches into a heuristic verdict."""
        pass
