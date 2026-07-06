"""Tests for spam heuristics."""

from ontology.domain.entities.email_signal import EmailSignal
from ontology.domain.services.spam_heuristics import classify_with_heuristics
from ontology.domain.value_objects.spam_label import SpamLabel


def test_ham_for_normal_email() -> None:
    signal = EmailSignal(
        sender="team@company.com",
        subject="주간 회의 안내",
        body="내일 10시에 회의가 있습니다.",
    )
    verdict = classify_with_heuristics(signal)
    assert verdict.label == SpamLabel.HAM
    assert not verdict.is_blocked


def test_phishing_for_credential_lure() -> None:
    signal = EmailSignal(
        sender="noreply@fake-bank.com",
        subject="URGENT: Verify your account",
        body="Click here to verify your account immediately.",
    )
    verdict = classify_with_heuristics(signal)
    assert verdict.label == SpamLabel.PHISHING
    assert verdict.is_blocked
