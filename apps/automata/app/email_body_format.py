from __future__ import annotations

import html
import re

_SENTENCE_BREAK = re.compile(r"(?<=[.!?。？！])\s*")


def format_email_body(body: str) -> str:
    """Normalize line breaks and insert paragraph gaps when the model outputs a wall of text."""
    text = body.replace("\r\n", "\n").strip()
    text = re.sub(r"\n{3,}", "\n\n", text)

    if text.count("\n") >= 2:
        return text

    parts = [part.strip() for part in _SENTENCE_BREAK.split(text) if part.strip()]
    if len(parts) >= 2:
        return "\n\n".join(parts)
    return text


def email_body_to_html(body: str) -> str:
    paragraphs = [part.strip() for part in format_email_body(body).split("\n\n") if part.strip()]
    if not paragraphs:
        return ""

    chunks: list[str] = []
    for paragraph in paragraphs:
        lines = [html.escape(line) for line in paragraph.split("\n")]
        inner = "<br>".join(lines)
        chunks.append(
            f'<p style="margin:0 0 1em 0;line-height:1.6;">{inner}</p>',
        )
    return "".join(chunks)
