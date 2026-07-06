"""Neo4j driver bootstrap — shared across domain apps."""

from __future__ import annotations

from functools import lru_cache
import logging
import os

from neo4j import Driver, GraphDatabase

logger = logging.getLogger(__name__)

DEFAULT_NEO4J_URI = "bolt://localhost:7687"
DEFAULT_NEO4J_USER = "neo4j"
DEFAULT_NEO4J_PASSWORD = "ragwatson"


def is_neo4j_configured() -> bool:
    return bool(os.getenv("NEO4J_URI", "").strip())


@lru_cache(maxsize=1)
def get_neo4j_driver() -> Driver | None:
    uri = os.getenv("NEO4J_URI", DEFAULT_NEO4J_URI).strip()
    user = os.getenv("NEO4J_USER", DEFAULT_NEO4J_USER).strip()
    password = os.getenv("NEO4J_PASSWORD", DEFAULT_NEO4J_PASSWORD).strip()
    try:
        driver = GraphDatabase.driver(
            uri,
            auth=(user, password),
            connection_timeout=5.0,
        )
        driver.verify_connectivity()
        logger.info("[Neo4j] connected uri=%s", uri)
        return driver
    except Exception:
        logger.warning("[Neo4j] unavailable uri=%s", uri)
        return None
