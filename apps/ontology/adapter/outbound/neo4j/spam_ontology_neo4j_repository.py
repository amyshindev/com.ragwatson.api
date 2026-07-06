from __future__ import annotations

import asyncio
import logging

from core.graph.neo4j_driver import get_neo4j_driver
from ontology.app.ports.output.spam_ontology_port import SpamOntologyPort
from ontology.domain.entities.email_signal import EmailSignal
from ontology.domain.entities.spam_verdict import SpamVerdict
from ontology.domain.ontologies.spam_taxonomy import SPAM_CONCEPTS
from ontology.domain.value_objects.spam_label import SpamLabel

logger = logging.getLogger(__name__)


class SpamOntologyNeo4jRepository(SpamOntologyPort):
    def __init__(self, fallback: SpamOntologyPort) -> None:
        self._fallback = fallback
        self._seeded = False

    async def enrich_verdict(self, signal: EmailSignal, base: SpamVerdict) -> SpamVerdict:
        driver = get_neo4j_driver()
        if driver is None:
            return await self._fallback.enrich_verdict(signal, base)

        try:
            await asyncio.to_thread(self._ensure_seed, driver)
            graph_hits = await asyncio.to_thread(self._match_concepts, driver, signal)
            if not graph_hits:
                return base
            return self._merge_hits(base, graph_hits)
        except Exception:
            logger.exception("[SpamOntologyNeo4jRepository] graph query failed")
            return await self._fallback.enrich_verdict(signal, base)

    def _ensure_seed(self, driver) -> None:
        if self._seeded:
            return
        from ontology.domain.ontologies.spam_taxonomy import KEYWORD_TO_CONCEPT

        with driver.session() as session:
            for keyword, concept_id in KEYWORD_TO_CONCEPT.items():
                label, reason = SPAM_CONCEPTS[concept_id]
                session.run(
                    """
                    MERGE (c:SpamConcept {id: $id})
                    SET c.keyword = $keyword, c.reason = $reason
                    WITH c
                    MERGE (cat:SpamCategory {name: $category})
                    MERGE (c)-[:INDICATES]->(cat)
                    """,
                    id=concept_id,
                    keyword=keyword.lower(),
                    reason=reason,
                    category=label.value,
                )
        self._seeded = True

    def _match_concepts(self, driver, signal: EmailSignal) -> list[dict[str, str]]:
        text = signal.combined_text
        with driver.session() as session:
            result = session.run(
                """
                MATCH (c:SpamConcept)-[:INDICATES]->(cat:SpamCategory)
                WHERE $text CONTAINS c.keyword
                RETURN c.id AS concept_id, cat.name AS category, c.reason AS reason
                """,
                text=text,
            )
            return [record.data() for record in result]

    def _merge_hits(self, base: SpamVerdict, hits: list[dict[str, str]]) -> SpamVerdict:
        reasons = list(base.reasons)
        concepts = list(base.matched_concepts)
        label_scores: dict[SpamLabel, float] = dict.fromkeys(SpamLabel, 0.0)
        label_scores[base.label] = base.score

        for hit in hits:
            concept_id = hit["concept_id"]
            category = hit["category"]
            reason = hit.get("reason") or concept_id
            try:
                label = SpamLabel(category)
            except ValueError:
                label = SpamLabel.SPAM
            label_scores[label] += 0.1
            if concept_id not in concepts:
                concepts.append(concept_id)
                reasons.append(f"Neo4j 온톨로지: {reason}")

        best_label = max(
            (SpamLabel.PHISHING, SpamLabel.SPAM, SpamLabel.PROMO, SpamLabel.HAM),
            key=lambda lbl: label_scores[lbl],
        )
        return SpamVerdict(
            label=best_label,
            score=round(min(max(label_scores[best_label], base.score), 1.0), 2),
            reasons=tuple(reasons),
            matched_concepts=tuple(concepts),
        )
