"""Central place for API keys and external client wiring (Gemini, future providers)."""

from __future__ import annotations

import os
from pathlib import Path

import google.generativeai as genai

from core.config import _ensure_env_loaded


class Keymaker:
    """Loads secrets from the environment and configures SDK clients."""

    def __init__(self) -> None:
        self.gemini_model_name: str = "gemini-2.5-flash"
        self._gemini_key: str = ""
        self._gemini_model: genai.GenerativeModel | None = None

    def bootstrap(self, *, env_file: Path | None = None) -> None:
        """Load `.env` (optional path) then wire all clients. Safe to call more than once."""
        from dotenv import load_dotenv

        if env_file is not None and env_file.is_file():
            load_dotenv(env_file)
        else:
            _ensure_env_loaded()
        self.refresh()

    def refresh(self) -> None:
        """Re-read environment variables and reconfigure clients."""
        self._gemini_key = (os.getenv("GEMINI_API_KEY") or "").strip()
        self._gemini_model = None
        if self._gemini_key:
            genai.configure(api_key=self._gemini_key)
            self._gemini_model = genai.GenerativeModel(self.gemini_model_name)

    def has_gemini(self) -> bool:
        return bool(self._gemini_key)

    def get_gemini_model(self) -> genai.GenerativeModel | None:
        return self._gemini_model


keymaker = Keymaker()
