"""T1 mid Faker — ExaONE 3.5 2.4B local orchestrator (Ollama).

사전 준비:
    ollama pull exaone3.5:2.4b
    ollama run exaone3.5:2.4b
"""

from __future__ import annotations

from dataclasses import dataclass, field
import logging
import os
from typing import Any

import ollama

logger = logging.getLogger(__name__)

DEFAULT_EXAONE_MODEL = "exaone3.5:2.4b"
DEFAULT_OLLAMA_HOST = "http://127.0.0.1:11434"


def _ollama_host() -> str:
    return (
        os.getenv("OLLAMA_BASE_URL")
        or os.getenv("OLLAMA_HOST")
        or DEFAULT_OLLAMA_HOST
    ).strip()


def _ollama_client() -> ollama.Client:
    return ollama.Client(host=_ollama_host())


def _model_name(entry: dict[str, Any]) -> str:
    return str(entry.get("model") or entry.get("name") or "")


@dataclass
class T1MidFakerOrchestrator:
    """Route chat requests to ExaONE on a local Ollama server."""

    model: str = field(
        default_factory=lambda: (os.getenv("EXAONE_MODEL") or DEFAULT_EXAONE_MODEL).strip()
    )
    _ready: bool = field(default=False, init=False)

    def register(self) -> bool:
        """Verify Ollama + ExaONE model, then mark this orchestrator ready."""
        if not self._ollama_reachable():
            logger.warning("[FakerOrchestrator] Ollama server unreachable")
            self._ready = False
            return False

        if not self._model_pulled():
            logger.warning(
                "[FakerOrchestrator] model not found: %s (run: ollama pull %s)",
                self.model,
                self.model,
            )
            self._ready = False
            return False

        self._ready = True
        logger.info("[FakerOrchestrator] registered model=%s", self.model)
        return True

    def is_ready(self) -> bool:
        return self._ready

    def chat(self, message: str, *, system: str | None = None) -> str:
        if not self._ready and not self.register():
            raise RuntimeError(
                f"ExaONE orchestrator is not ready. "
                f"Start Ollama and run: ollama pull {self.model}"
            )

        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": message})

        client = _ollama_client()
        response = client.chat(model=self.model, messages=messages)
        return str(response["message"]["content"])

    def _ollama_reachable(self) -> bool:
        try:
            _ollama_client().list()
            return True
        except Exception:
            return False

    def _model_pulled(self) -> bool:
        try:
            models = _ollama_client().list().get("models", [])
        except Exception:
            return False

        prefix = self.model.split(":")[0]
        return any(_model_name(m) == self.model or _model_name(m).startswith(f"{prefix}:") for m in models)


# alias → orchestrator (exaone, faker, …)
ORCHESTRATORS: dict[str, T1MidFakerOrchestrator] = {}


faker_orchestrator = T1MidFakerOrchestrator()


def register_exaone_orchestrator(
    *,
    model: str | None = None,
    alias: str = "exaone",
) -> T1MidFakerOrchestrator:
    """Register ExaONE as a named orchestrator in ``ORCHESTRATORS``."""
    orchestrator = faker_orchestrator if model is None else T1MidFakerOrchestrator(model=model)
    orchestrator.register()
    ORCHESTRATORS[alias] = orchestrator
    ORCHESTRATORS["faker"] = orchestrator
    return orchestrator


def get_orchestrator(alias: str = "exaone") -> T1MidFakerOrchestrator:
    if alias not in ORCHESTRATORS:
        raise KeyError(f"Orchestrator not registered: {alias}")
    return ORCHESTRATORS[alias]


__all__ = [
    "DEFAULT_EXAONE_MODEL",
    "DEFAULT_OLLAMA_HOST",
    "ORCHESTRATORS",
    "T1MidFakerOrchestrator",
    "faker_orchestrator",
    "get_orchestrator",
    "register_exaone_orchestrator",
]
