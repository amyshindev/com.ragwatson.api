"""Backward-compatible re-export. Prefer ``core.matrix.oracle_database``."""

from core.matrix.oracle_database import get_db

__all__ = ["get_db"]
