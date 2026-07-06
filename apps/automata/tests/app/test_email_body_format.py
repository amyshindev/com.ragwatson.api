"""Tests for email body formatting."""

from automata.app.email_body_format import email_body_to_html, format_email_body


def test_format_email_body_splits_wall_of_text() -> None:
    raw = (
        "안녕하세요. 프로젝트 진행이 순조롭습니다. "
        "다음 주에 결과를 공유드리겠습니다. 감사합니다."
    )
    body = format_email_body(raw)
    assert "\n\n" in body
    assert body.startswith("안녕하세요.")


def test_format_email_body_preserves_existing_paragraphs() -> None:
    raw = "안녕하세요.\n\n본문입니다.\n\n감사합니다."
    assert format_email_body(raw) == raw


def test_email_body_to_html_wraps_paragraphs() -> None:
    html_body = email_body_to_html("안녕하세요.\n\n감사합니다.")
    assert "<p" in html_body
    assert "<br>" not in html_body or "안녕하세요." in html_body
