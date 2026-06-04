from __future__ import annotations

from dataclasses import dataclass

from titanic.adapter.inbound.api.schemas.walter_schema import WalterSchema


@dataclass
class WalterQuery:
    """WalterSchema 컬럼 값을 앱 레이어로 전달."""

    id: int = 1
    name: str = "Walter"
    memo: str = "월터는 타이타닉의 승무원이다."

    @classmethod
    def from_schema(cls, schema: WalterSchema) -> WalterQuery:
        return cls(
            id=schema.id,
            name=schema.name,
            memo=schema.memo,
        )
