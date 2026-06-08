"""Backward-compatible re-export. Prefer ``core.database.secret_manager``."""

from core.database.secret_manager import Keymaker, keymaker

__all__ = ["Keymaker", "keymaker"]
