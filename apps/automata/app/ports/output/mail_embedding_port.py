from __future__ import annotations

from abc import ABC, abstractmethod


class MailEmbeddingPort(ABC):
    @abstractmethod
    def embed_mail_text(self, text: str) -> list[float]:
        pass
