from __future__ import annotations

import logging
import os

import ollama

from automata.adapter.outbound.orm.automata_inbound_mail_orm import MAIL_EMBEDDING_DIM
from automata.app.ports.output.mail_embedding_port import MailEmbeddingPort

log = logging.getLogger(__name__)

_DEFAULT_MODEL = "nomic-embed-text"


def build_mail_embedding_text(
    *,
    from_email: str,
    from_name: str | None,
    subject: str,
    body: str,
) -> str:
    sender = from_name.strip() if from_name else from_email
    parts = [f"From: {sender}", f"Subject: {subject.strip()}", body.strip()]
    return "\n\n".join(part for part in parts if part)


class OllamaMailEmbeddingAdapter(MailEmbeddingPort):
    def __init__(
        self,
        *,
        model: str | None = None,
        dimensions: int = MAIL_EMBEDDING_DIM,
    ) -> None:
        self._model = (model or os.getenv("OLLAMA_EMBED_MODEL") or _DEFAULT_MODEL).strip()
        self._dimensions = dimensions
        host = (
            os.getenv("OLLAMA_BASE_URL")
            or os.getenv("OLLAMA_HOST")
            or "http://127.0.0.1:11434"
        ).strip()
        self._client = ollama.Client(host=host)

    def embed_mail_text(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("임베딩할 메일 본문이 비어 있습니다.")

        response = self._client.embed(model=self._model, input=text)
        embeddings = response.get("embeddings") or []
        if not embeddings or not embeddings[0]:
            raise RuntimeError(f"Ollama 임베딩 응답이 비어 있습니다. model={self._model}")

        vector = [float(value) for value in embeddings[0]]
        if len(vector) != self._dimensions:
            raise RuntimeError(
                f"임베딩 차원 불일치: expected={self._dimensions}, got={len(vector)}",
            )

        log.info("[OllamaMailEmbeddingAdapter] embedded chars=%s dim=%s", len(text), len(vector))
        return vector
