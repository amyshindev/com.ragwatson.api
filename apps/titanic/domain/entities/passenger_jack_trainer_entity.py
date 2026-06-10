from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from titanic.domain.value_objects.passenger_jack_trainer_vo import Age, FamilySize, PassengerName

if TYPE_CHECKING:
    from titanic.domain.entities.passenger_rose_model_entity import Booking

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"

class SurvivalStatus(Enum):
    PERISHED = 0
    SURVIVED = 1

class Passenger:
    """타이타닉 승객 도메인 엔티티"""
    
    def __init__(
        self,
        passenger_id: int,  # 식별자
        name: PassengerName,  # VO
        gender: Gender,       # Enum
        age: Optional[Age],   # VO (결측치 허용)
        family: FamilySize,   # VO
        survival_status: SurvivalStatus,
        bookings: Optional[List["Booking"]] = None
    ):
        self._passenger_id = passenger_id
        self.name = name
        self.gender = gender
        self.age = age
        self.family = family
        self.survival_status = survival_status
        self.bookings = bookings or []

    @property
    def passenger_id(self) -> int:
        return self._passenger_id

    # 엔티티의 동일성은 오직 식별자(ID)로만 판단합니다.
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Passenger):
            return False
        return self._passenger_id == other._passenger_id

    # --- 비즈니스 로직 (도메인 메서드) ---
    def change_name(self, new_name: PassengerName):
        """이름 변경 등의 비즈니스 행위"""
        self.name = new_name

    def is_child(self) -> bool:
        """아이인지 여부를 확인하는 도메인 로직"""
        if self.age is None:
            return False
        return self.age.value < 16