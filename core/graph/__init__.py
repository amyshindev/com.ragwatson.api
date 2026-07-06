"""Shared graph database infrastructure (Neo4j)."""

from core.graph.neo4j_driver import get_neo4j_driver, is_neo4j_configured

__all__ = ["get_neo4j_driver", "is_neo4j_configured"]
