from __future__ import annotations

import re

from ontology.domain.entities.email_signal import EmailSignal
from ontology.domain.entities.spam_verdict import SpamVerdict
from ontology.domain.ontologies.spam_taxonomy import KEYWORD_TO_CONCEPT, SPAM_CONCEPTS
from ontology.domain.value_objects.spam_label import SpamLabel

_LABEL_PRIORITY = (
    SpamLabel.PHISHING,
    SpamLabel.SPAM,
    SpamLabel.PROMO,
    SpamLabel.HAM,
)

_URL_PATTERN = re.compile(r"https?://", re.IGNORECASE)


def classify_with_heuristics(signal: EmailSignal) -> SpamVerdict:
    text = signal.combined_text
    reasons: list[str] = []
    matched: list[str] = []
    label_scores: dict[SpamLabel, float] = dict.fromkeys(SpamLabel, 0.0)

    for keyword, concept_id in KEYWORD_TO_CONCEPT.items():
        if keyword in text:
            label, reason = SPAM_CONCEPTS[concept_id]
            label_scores[label] += 0.25
            matched.append(concept_id)
            reasons.append(f"{reason} (키워드: {keyword!r})")

    url_count = len(_URL_PATTERN.findall(text))
    if url_count >= 3:
        label_scores[SpamLabel.PHISHING] += 0.3
        reasons.append(f"피싱 의심: URL {url_count}개")

    if signal.subject.isupper() and len(signal.subject) > 10:
        label_scores[SpamLabel.SPAM] += 0.15
        reasons.append("스팸 의심: 제목 전체 대문자")

    if text.count("!") >= 5:
        label_scores[SpamLabel.PROMO] += 0.1
        reasons.append("프로모 의심: 과도한 느낌표")

    best_label = max(_LABEL_PRIORITY, key=lambda lbl: label_scores[lbl])
    best_score = label_scores[best_label]

    if best_score < 0.2:
        return SpamVerdict(
            label=SpamLabel.HAM,
            score=round(1.0 - best_score, 2),
            reasons=tuple(reasons) if reasons else ("정상 메일로 분류",),
            matched_concepts=tuple(dict.fromkeys(matched)),
        )

    return SpamVerdict(
        label=best_label,
        score=round(min(best_score, 1.0), 2),
        reasons=tuple(reasons),
        matched_concepts=tuple(dict.fromkeys(matched)),
    )
