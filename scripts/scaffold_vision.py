"""Scaffold backend/apps/vision hexagonal slices (sherlock_holmes pattern)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "vision"

CHARACTERS: list[dict[str, str]] = [
    {
        "stem": "optic_yolo_detector",
        "route": "yolo",
        "tag": "yolo",
        "class_stem": "YoloDetector",
        "display_name": "요로 (YOLO)",
        "role_line": "실시간 객체 탐지",
    },
    {
        "stem": "optic_resnet_classifier",
        "route": "resnet",
        "tag": "resnet",
        "class_stem": "ResnetClassifier",
        "display_name": "레즈넷 (ResNet)",
        "role_line": "이미지 분류",
    },
    {
        "stem": "optic_sam_segmenter",
        "route": "sam",
        "tag": "sam",
        "class_stem": "SamSegmenter",
        "display_name": "샘 (SAM)",
        "role_line": "세그멘테이션",
    },
    {
        "stem": "optic_clip_embedder",
        "route": "clip",
        "tag": "clip",
        "class_stem": "ClipEmbedder",
        "display_name": "클립 (CLIP)",
        "role_line": "멀티모달 임베딩·유사도",
    },
    {
        "stem": "optic_ocr_reader",
        "route": "ocr",
        "tag": "ocr",
        "class_stem": "OcrReader",
        "display_name": "OCR 리더",
        "role_line": "문자·텍스트 인식",
    },
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


def scaffold_character(char: dict[str, str]) -> list[str]:
    stem = char["stem"]
    route = char["route"]
    tag = char["tag"]
    class_stem = char["class_stem"]
    display_name = char["display_name"]
    role_line = char["role_line"]
    router_var = f"{stem}_router"

    write(
        APP / "adapter/inbound/api/schemas" / f"{stem}_schema.py",
        f'''from pydantic import BaseModel, Field


class {class_stem}Schema(BaseModel):
    id: int = Field(1, description="Character ID")
    name: str = Field("{display_name}", description="Character name")

    model_config = {{
        "json_schema_extra": {{
            "example": {{
                "id": 1,
                "name": "{display_name}",
            }}
        }}
    }}
''',
    )

    write(
        APP / "app/dtos" / f"{stem}_dto.py",
        f'''from dataclasses import dataclass


@dataclass(frozen=True)
class {class_stem}Query:
    id: int
    name: str


@dataclass(frozen=True)
class {class_stem}Response:
    id: int
    name: str
''',
    )

    write(
        APP / "app/ports/input" / f"{stem}_use_case.py",
        f'''from __future__ import annotations

from abc import ABC, abstractmethod

from vision.adapter.inbound.api.schemas.{stem}_schema import {class_stem}Schema
from vision.app.dtos.{stem}_dto import {class_stem}Response


class {class_stem}UseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: {class_stem}Schema) -> {class_stem}Response:
        """{display_name} 자기소개"""
        pass
''',
    )

    write(
        APP / "app/ports/output" / f"{stem}_port.py",
        f'''from __future__ import annotations

from abc import ABC, abstractmethod

from vision.app.dtos.{stem}_dto import {class_stem}Query, {class_stem}Response


class {class_stem}Port(ABC):
    @abstractmethod
    async def introduce_myself(self, query: {class_stem}Query) -> {class_stem}Response:
        """{display_name} 저장소"""
        pass
''',
    )

    write(
        APP / "app/use_cases" / f"{stem}_interactor.py",
        f'''from __future__ import annotations

from vision.adapter.inbound.api.schemas.{stem}_schema import {class_stem}Schema
from vision.app.dtos.{stem}_dto import {class_stem}Query, {class_stem}Response
from vision.app.ports.input.{stem}_use_case import {class_stem}UseCase
from vision.app.ports.output.{stem}_port import {class_stem}Port


class {class_stem}Interactor({class_stem}UseCase):
    def __init__(self, repository: {class_stem}Port) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: {class_stem}Schema) -> {class_stem}Response:
        return await self._repository.introduce_myself(
            {class_stem}Query(id=schema.id, name=schema.name)
        )
''',
    )

    write(
        APP / "adapter/outbound/pg" / f"{stem}_repository.py",
        f'''from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from vision.app.dtos.{stem}_dto import {class_stem}Query, {class_stem}Response
from vision.app.ports.output.{stem}_port import {class_stem}Port

log = logging.getLogger(__name__)


class {class_stem}PgRepository({class_stem}Port):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(self, query: {class_stem}Query) -> {class_stem}Response:
        log.info("[{class_stem}PgRepository] introduce_myself id=%s", query.id)
        return {class_stem}Response(
            id=query.id,
            name=f"{{query.name}} — {role_line}",
        )
''',
    )

    write(
        APP / "dependencies" / f"{stem}_provider.py",
        f'''from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from vision.adapter.outbound.pg.{stem}_repository import {class_stem}PgRepository
from vision.app.ports.input.{stem}_use_case import {class_stem}UseCase
from vision.app.ports.output.{stem}_port import {class_stem}Port
from vision.app.use_cases.{stem}_interactor import {class_stem}Interactor


def get_{stem}_repository(
    db: AsyncSession = Depends(get_db),
) -> {class_stem}Port:
    return {class_stem}PgRepository(session=db)


def get_{stem}_use_case(
    repository: {class_stem}Port = Depends(get_{stem}_repository),
) -> {class_stem}UseCase:
    return {class_stem}Interactor(repository=repository)
''',
    )

    write(
        APP / "adapter/inbound/api/v1" / f"{stem}_router.py",
        f'''from fastapi import APIRouter, Depends

from vision.adapter.inbound.api.schemas.{stem}_schema import {class_stem}Schema
from vision.app.dtos.{stem}_dto import {class_stem}Response
from vision.app.ports.input.{stem}_use_case import {class_stem}UseCase
from vision.dependencies.{stem}_provider import get_{stem}_use_case

{router_var} = APIRouter(prefix="/vision/{route}", tags=["vision", "{tag}"])


@{router_var}.get("/myself")
async def introduce_myself(
    character: {class_stem}UseCase = Depends(get_{stem}_use_case),
) -> {class_stem}Response:
    return await character.introduce_myself(
        {class_stem}Schema(id=1, name="{display_name}")
    )
''',
    )

    return [router_var]


def scaffold_app(router_vars: list[str]) -> None:
    for name in [
        "",
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
        "domain",
        "tests",
        "_docs",
    ]:
        init = APP / name / "__init__.py" if name else APP / "__init__.py"
        if not init.exists():
            write(init, "")

    imports = "\n".join(
        f"from vision.adapter.inbound.api.v1.{char['stem']}_router import {char['stem']}_router"
        for char in CHARACTERS
    )
    includes = "\n".join(
        f"vision_router.include_router({char['stem']}_router)" for char in CHARACTERS
    )
    write(
        APP / "adapter/inbound/api/router_registry.py",
        f'''from fastapi import APIRouter

{imports}

vision_router = APIRouter()
{includes}

__all__ = ["vision_router"]
''',
    )

    table_rows = "\n".join(
        f"| `{c['stem']}` | `/vision/{c['route']}` | {c['role_line']} |"
        for c in CHARACTERS
    )
    route_rows = "\n".join(
        f"- `GET /vision/{c['route']}/myself` — {c['display_name']}"
        for c in CHARACTERS
    )
    write(
        APP / "_docs/CLAUDE.md",
        f'''---
tags:
  - harness/claude-vision
graph-group: claude-vision
---

# Vision App — CLAUDE.md

`backend/apps/vision/` — Sherlock Holmes / Titanic과 동일한 Hexagonal + Vertical Slice.

> **Import:** `from vision.adapter...` (`PYTHONPATH=apps`)

## 캐릭터 (introduce_myself)

| stem | prefix | 역할 |
|------|--------|------|
{table_rows}

각 캐릭터: `GET /vision/{{name}}/myself` → `{{ id, name }}`.

## 라우트

{route_rows}

## 슬라이스 파일 세트

`{{stem}}_router.py` 기준으로 schema, dto, ports, interactor, provider, pg repository가 동일 stem으로 쌍을 이룹니다.

## References

- Titanic 아키텍처: [`../titanic/_docs/structure.md`](../titanic/_docs/structure.md)
''',
    )


def main() -> None:
    print(f"Scaffolding vision app at {APP}")
    router_vars: list[str] = []
    for char in CHARACTERS:
        print(f"\n[{char['stem']}]")
        router_vars.extend(scaffold_character(char))
    scaffold_app(router_vars)
    print("\nDone. Register in backend/main.py:")
    print("  from vision.adapter.inbound.api.router_registry import vision_router")
    print("  app.include_router(vision_router)")


if __name__ == "__main__":
    main()
