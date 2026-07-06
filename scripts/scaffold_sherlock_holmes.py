"""Scaffold sherlock_holmes app slices from router stems (introduce_myself only)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "apps" / "sherlock_holmes"

APP = "sherlock_holmes"
PREFIX = "/sherlock"

CHARACTERS = [
    {
        "stem": "detective_sherlock_holmes",
        "route": "holmes",
        "tag": "holmes",
        "prefix": "SherlockHolmes",
        "router_var": "detective_sherlock_holmes_router",
        "id": 1,
        "name": "셜록 홈즈 (Sherlock Holmes)",
        "schema_name": "셜록 홈즈",
        "note": "베이커가 221B, 추론·단서 분석",
    },
    {
        "stem": "doctor_watson_chronicler",
        "route": "watson",
        "tag": "watson",
        "prefix": "WatsonChronicler",
        "router_var": "watson_chronicler_router",
        "id": 2,
        "name": "존 H. 왓슨 (Dr. John Watson)",
        "schema_name": "왓슨",
        "note": "동반자·사건 기록자",
    },
    {
        "stem": "inspector_lestrade_official",
        "route": "lestrade",
        "tag": "lestrade",
        "prefix": "LestradeOfficial",
        "router_var": "lestrade_official_router",
        "id": 3,
        "name": "인스펙터 레스트레이드 (Inspector Lestrade)",
        "schema_name": "레스트레이드",
        "note": "스코트랜드야드 공식 수사",
    },
    {
        "stem": "mrs_hudson_housekeeper",
        "route": "hudson",
        "tag": "hudson",
        "prefix": "HudsonHousekeeper",
        "router_var": "hudson_housekeeper_router",
        "id": 4,
        "name": "미스 허드슨 (Mrs. Hudson)",
        "schema_name": "허드슨",
        "note": "221B 하우스키퍼·현장 접수",
    },
    {
        "stem": "brother_mycroft_strategist",
        "route": "mycroft",
        "tag": "mycroft",
        "prefix": "MycroftStrategist",
        "router_var": "mycroft_strategist_router",
        "id": 5,
        "name": "마이크로프트 홈즈 (Mycroft Holmes)",
        "schema_name": "마이크로프트",
        "note": "전략·정보 조율",
    },
    {
        "stem": "professor_moriarty_rival",
        "route": "moriarty",
        "tag": "moriarty",
        "prefix": "MoriartyRival",
        "router_var": "moriarty_rival_router",
        "id": 6,
        "name": "프로페서 모리어티 (Professor Moriarty)",
        "schema_name": "모리어티",
        "note": "적대 검증·리스크 시나리오",
    },
]


def w(path: str, content: str) -> None:
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")


def schema_file(c: dict) -> str:
    p = c["prefix"]
    return f'''from pydantic import BaseModel, Field


class {p}Schema(BaseModel):
    id: int = Field({c["id"]}, description="Character ID")
    name: str = Field("{c["schema_name"]}", description="Character name")
    # {c["note"]}

    model_config = {{
        "json_schema_extra": {{
            "example": {{
                "id": {c["id"]},
                "name": "{c["name"]}",
            }}
        }}
    }}
'''


def dto_file(c: dict) -> str:
    p = c["prefix"]
    alias = "".join(part.capitalize() for part in c["stem"].split("_"))
    return f'''from dataclasses import dataclass


@dataclass(frozen=True)
class {p}Query:
    id: int
    name: str


@dataclass(frozen=True)
class {p}Response:
    id: int
    name: str


{alias}Query = {p}Query
{alias}Response = {p}Response
'''


def use_case_input(c: dict) -> str:
    p = c["prefix"]
    stem = c["stem"]
    alias = "".join(part.capitalize() for part in stem.split("_"))
    return f'''from __future__ import annotations

from abc import ABC, abstractmethod

from {APP}.adapter.inbound.api.schemas.{stem}_schema import {p}Schema
from {APP}.app.dtos.{stem}_dto import {p}Response


class {p}UseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: {p}Schema) -> {p}Response:
        """{c["schema_name"]} 자기소개"""
        pass


{alias}UseCase = {p}UseCase
'''


def port_output(c: dict) -> str:
    p = c["prefix"]
    stem = c["stem"]
    alias = "".join(part.capitalize() for part in stem.split("_"))
    return f'''from __future__ import annotations

from abc import ABC, abstractmethod

from {APP}.app.dtos.{stem}_dto import {p}Query, {p}Response


class {p}Port(ABC):
    @abstractmethod
    async def introduce_myself(self, query: {p}Query) -> {p}Response:
        """{c["schema_name"]} 자기소개 저장소"""
        pass


{alias}Port = {p}Port
'''


def interactor(c: dict) -> str:
    p = c["prefix"]
    stem = c["stem"]
    alias = "".join(part.capitalize() for part in stem.split("_"))
    return f'''from __future__ import annotations

from {APP}.adapter.inbound.api.schemas.{stem}_schema import {p}Schema
from {APP}.app.dtos.{stem}_dto import {p}Query, {p}Response
from {APP}.app.ports.input.{stem}_use_case import {p}UseCase
from {APP}.app.ports.output.{stem}_port import {p}Port


class {p}Interactor({p}UseCase):
    def __init__(self, repository: {p}Port) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: {p}Schema) -> {p}Response:
        return await self._repository.introduce_myself(
            {p}Query(id=schema.id, name=schema.name)
        )


{alias}Interactor = {p}Interactor
'''


def repository(c: dict) -> str:
    p = c["prefix"]
    stem = c["stem"]
    alias = "".join(part.capitalize() for part in stem.split("_"))
    return f'''from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from {APP}.app.dtos.{stem}_dto import {p}Query, {p}Response
from {APP}.app.ports.output.{stem}_port import {p}Port

log = logging.getLogger(__name__)


class {p}PgRepository({p}Port):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: {p}Query) -> {p}Response:
        log.info("[{p}PgRepository] introduce_myself id=%s", query.id)
        return {p}Response(
            id=query.id,
            name=f"{{query.name}} — {c["note"]}",
        )


{alias}PgRepository = {p}PgRepository
'''


def provider(c: dict) -> str:
    p = c["prefix"]
    stem = c["stem"]
    return f'''from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from {APP}.adapter.outbound.pg.{stem}_repository import {p}PgRepository
from {APP}.app.ports.input.{stem}_use_case import {p}UseCase
from {APP}.app.ports.output.{stem}_port import {p}Port
from {APP}.app.use_cases.{stem}_interactor import {p}Interactor


def get_{stem}_repository(
    db: AsyncSession = Depends(get_db),
) -> {p}Port:
    return {p}PgRepository(session=db)


def get_{stem}_use_case(
    repository: {p}Port = Depends(get_{stem}_repository),
) -> {p}UseCase:
    return {p}Interactor(repository=repository)
'''


def router(c: dict) -> str:
    p = c["prefix"]
    stem = c["stem"]
    dep = f"get_{stem}_use_case"
    return f'''from fastapi import APIRouter, Depends

from {APP}.adapter.inbound.api.schemas.{stem}_schema import {p}Schema
from {APP}.app.dtos.{stem}_dto import {p}Response
from {APP}.app.ports.input.{stem}_use_case import {p}UseCase
from {APP}.dependencies.{stem}_provider import {dep}

{c["router_var"]} = APIRouter(prefix="{PREFIX}/{c["route"]}", tags=["{c["tag"]}"])


@{c["router_var"]}.get("/myself")
async def introduce_myself(
    character: {p}UseCase = Depends({dep}),
) -> {p}Response:
    return await character.introduce_myself(
        {p}Schema(id={c["id"]}, name="{c["name"]}")
    )
'''


def main() -> None:
    for c in CHARACTERS:
        stem = c["stem"]
        w(f"adapter/inbound/api/schemas/{stem}_schema.py", schema_file(c))
        w(f"app/dtos/{stem}_dto.py", dto_file(c))
        w(f"app/ports/input/{stem}_use_case.py", use_case_input(c))
        w(f"app/ports/output/{stem}_port.py", port_output(c))
        w(f"app/use_cases/{stem}_interactor.py", interactor(c))
        w(f"adapter/outbound/pg/{stem}_repository.py", repository(c))
        w(f"dependencies/{stem}_provider.py", provider(c))
        w(f"adapter/inbound/api/v1/{stem}_router.py", router(c))

    imports = "\n".join(
        f"from {APP}.adapter.inbound.api.v1.{c['stem']}_router import {c['router_var']}"
        for c in CHARACTERS
    )
    includes = "\n".join(
        f"sherlock_holmes_router.include_router({c['router_var']})" for c in CHARACTERS
    )
    registry = f'''from fastapi import APIRouter

{imports}

sherlock_holmes_router = APIRouter()
{includes}

__all__ = ["sherlock_holmes_router"]
'''
    w("adapter/inbound/api/router_registry.py", registry)
    w("__init__.py", "")
    for pkg in [
        "adapter",
        "adapter/inbound",
        "adapter/inbound/api",
        "adapter/inbound/api/schemas",
        "adapter/inbound/api/v1",
        "adapter/outbound",
        "adapter/outbound/pg",
        "app",
        "app/dtos",
        "app/ports",
        "app/ports/input",
        "app/ports/output",
        "app/use_cases",
        "dependencies",
    ]:
        w(f"{pkg}/__init__.py", "")

    print(f"Generated {len(CHARACTERS)} character slices under {ROOT}")


if __name__ == "__main__":
    main()
