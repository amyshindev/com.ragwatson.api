from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database.grid_neo_theone_base import Base


class AutomataContactOrm(Base):
    __tablename__ = "automata_contacts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
