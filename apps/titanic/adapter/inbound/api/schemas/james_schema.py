from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from titanic.domain.entities.titanic import TitanicPassenger

JAMES_UPLOAD_COLUMNS: list[str] = [
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "Gender",
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
]


class JamesPassengerRow(BaseModel):
    """타이타닉 승객 생성/검증 요청 (James CSV 업로드)."""

    passenger_id: int = Field(..., alias="PassengerId", description="승객 ID")
    survived: int = Field(..., alias="Survived", description="생존 여부 (0 = 사망, 1 = 생존)")
    pclass: int = Field(..., alias="Pclass", description="티켓 클래스 (1 = 1등석, 2 = 2등석, 3 = 3등석)")
    name: str = Field(..., alias="Name", description="이름")
    gender: str = Field(..., alias="Gender", description="성별")
    age: float | None = Field(default=None, alias="Age", description="나이")
    sibsp: int = Field(..., alias="SibSp", description="함께 탑승한 자녀 / 배우자의 수")
    parch: int = Field(..., alias="Parch", description="함께 탑승한 부모님 / 아이들의 수")
    ticket: str = Field(..., alias="Ticket", description="티켓 번호")
    fare: float = Field(..., alias="Fare", description="탑승 요금")
    cabin: str | None = Field(default=None, alias="Cabin", description="수하물 번호")
    boat: str | None = Field(default=None, alias="Boat", description="탈출한 보트 번호")
    embarked: str | None = Field(default=None, alias="Embarked", description="선착장 (C, Q, S)")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @classmethod
    def _normalize_payload(cls, data: dict[str, Any]) -> dict[str, Any]:
        payload = dict(data)
        if "Sex" in payload and "Gender" not in payload:
            payload["Gender"] = payload.pop("Sex")
        if "sex" in payload and "gender" not in payload and "Gender" not in payload:
            payload["gender"] = payload.pop("sex")
        return payload

    @classmethod
    def from_payload(cls, data: dict[str, Any]) -> JamesPassengerRow:
        return cls.model_validate(cls._normalize_payload(data))

    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> JamesPassengerRow:
        age_raw = (row.get("Age") or "").strip()
        return cls.model_validate(
            {
                "PassengerId": row.get("PassengerId", ""),
                "Survived": row.get("Survived", ""),
                "Pclass": row.get("Pclass", ""),
                "Name": row.get("Name", ""),
                "Gender": row.get("Gender") or row.get("Sex", ""),
                "Age": age_raw if age_raw else None,
                "SibSp": row.get("SibSp", ""),
                "Parch": row.get("Parch", ""),
                "Ticket": row.get("Ticket", ""),
                "Fare": row.get("Fare", ""),
                "Cabin": (row.get("Cabin") or "").strip() or None,
                "Boat": (row.get("Boat") or "").strip() or None,
                "Embarked": (row.get("Embarked") or "").strip() or None,
            }
        )

    def to_upload_row(self) -> dict[str, str]:
        return {
            "PassengerId": str(self.passenger_id),
            "Survived": str(self.survived),
            "Pclass": str(self.pclass),
            "Name": self.name,
            "Gender": self.gender,
            "Age": "" if self.age is None else str(self.age),
            "SibSp": str(self.sibsp),
            "Parch": str(self.parch),
            "Ticket": self.ticket,
            "Fare": str(self.fare),
            "Cabin": self.cabin or "",
            "Embarked": self.embarked or "",
        }

    def to_entity(self) -> TitanicPassenger:
        return TitanicPassenger(
            passenger_id=str(self.passenger_id),
            survived=str(self.survived),
            pclass=str(self.pclass),
            name=self.name,
            gender=self.gender,
            age="" if self.age is None else str(self.age),
            sibsp=str(self.sibsp),
            parch=str(self.parch),
            ticket=self.ticket,
            fare=str(self.fare),
            cabin=self.cabin or "",
            embarked=self.embarked or "",
        )


class JamesUploadResponse(BaseModel):
    filename: str
    count: int
    columns: list[str]
    items: list[dict[str, str]]
