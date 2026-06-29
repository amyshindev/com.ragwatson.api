"""Tests for faker_mailer email draft parsing."""

from automata.app.use_cases.faker_mailer_interactor import parse_email_draft


def test_parse_email_draft_subject_body_format() -> None:
    raw = "Subject: 안녕하세요\nBody:\n본문 첫 줄\n본문 둘째 줄"
    subject, body = parse_email_draft(raw)
    assert subject == "안녕하세요"
    assert "본문 첫 줄" in body


def test_parse_email_draft_fallback_subject() -> None:
    subject, body = parse_email_draft("단일 본문", fallback_subject="[Test]")
    assert subject == "[Test]"
    assert body == "단일 본문"
