"""Spam ontology concept → category mapping (nominal labels)."""

from __future__ import annotations

from ontology.domain.value_objects.spam_label import SpamLabel

# concept_id → (label, human-readable reason template)
SPAM_CONCEPTS: dict[str, tuple[SpamLabel, str]] = {
    "concept:phishing_credential": (SpamLabel.PHISHING, "피싱: 계정·비밀번호 탈취 유도"),
    "concept:phishing_urgency": (SpamLabel.PHISHING, "피싱: 긴급 행동 압박"),
    "concept:spam_lottery": (SpamLabel.SPAM, "스팸: 당첨·복권 사기"),
    "concept:spam_financial": (SpamLabel.SPAM, "스팸: 고수익·투자 유도"),
    "concept:promo_unsubscribe": (SpamLabel.PROMO, "프로모: 대량 마케팅"),
    "concept:promo_discount": (SpamLabel.PROMO, "프로모: 과도한 할인 광고"),
}

# keyword triggers → concept_id
KEYWORD_TO_CONCEPT: dict[str, str] = {
    "verify your account": "concept:phishing_credential",
    "password expired": "concept:phishing_credential",
    "계정 확인": "concept:phishing_credential",
    "비밀번호": "concept:phishing_credential",
    "urgent action": "concept:phishing_urgency",
    "immediately": "concept:phishing_urgency",
    "지금 바로": "concept:phishing_urgency",
    "you won": "concept:spam_lottery",
    "lottery": "concept:spam_lottery",
    "당첨": "concept:spam_lottery",
    "free money": "concept:spam_financial",
    "bitcoin": "concept:spam_financial",
    "고수익": "concept:spam_financial",
    "unsubscribe": "concept:promo_unsubscribe",
    "수신거부": "concept:promo_unsubscribe",
    "50% off": "concept:promo_discount",
    "할인": "concept:promo_discount",
}
