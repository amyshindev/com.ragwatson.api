from __future__ import annotations

from ontology.app.ports.output.spam_ontology_port import SpamOntologyPort
from ontology.domain.entities.email_signal import EmailSignal
from ontology.domain.entities.spam_verdict import SpamVerdict
from ontology.domain.ontologies.spam_taxonomy import KEYWORD_TO_CONCEPT, SPAM_CONCEPTS
from ontology.domain.value_objects.spam_label import SpamLabel


class SpamOntologyMemoryRepository(SpamOntologyPort):
    """In-memory taxonomy lookup — works without Neo4j."""

    async def enrich_verdict(self, signal: EmailSignal, base: SpamVerdict) -> SpamVerdict:
        text = signal.combined_text
        extra_concepts: list[str] = []
        extra_reasons: list[str] = list(base.reasons)
        label_scores: dict[SpamLabel, float] = dict.fromkeys(SpamLabel, 0.0)
        label_scores[base.label] = base.score

        for keyword, concept_id in KEYWORD_TO_CONCEPT.items():
            if keyword in text and concept_id not in base.matched_concepts:
                label, reason = SPAM_CONCEPTS[concept_id]
                label_scores[label] += 0.05
                extra_concepts.append(concept_id)
                extra_reasons.append(f"온톨로지 매칭: {reason}")

        if not extra_concepts:
            return base

        best_label = max(
            (SpamLabel.PHISHING, SpamLabel.SPAM, SpamLabel.PROMO, SpamLabel.HAM),
            key=lambda lbl: label_scores[lbl],
        )
        merged_concepts = tuple(dict.fromkeys((*base.matched_concepts, *extra_concepts)))
        return SpamVerdict(
            label=best_label,
            score=round(min(max(label_scores[best_label], base.score), 1.0), 2),
            reasons=tuple(extra_reasons),
            matched_concepts=merged_concepts,
        )
