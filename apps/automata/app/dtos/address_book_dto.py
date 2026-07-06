from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContactCommand:
    nickname: str
    email: str


@dataclass(frozen=True)
class ContactRow:
    id: int
    nickname: str
    email: str


@dataclass(frozen=True)
class ContactListResult:
    items: list[ContactRow]
    total: int
    page: int
    page_size: int
