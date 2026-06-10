from dataclasses import dataclass

@dataclass(frozen=True)
class PassengerName:
    """승객 이름 VO"""
    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("이름은 공백일 수 없습니다.")


@dataclass(frozen=True)
class Age:
    """나이 VO (데이터 세트 특성상 소수점이나 누락이 있을 수 있으므로 float/None 처리 고려)"""
    value: float

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("나이는 음수일 수 없습니다.")


@dataclass(frozen=True)
class FamilySize:
    """동반 가족 수 VO (SibSp, Parch 통합 또는 개별 적용 가능)"""
    sib_sp: int
    parch: int

    def __post_init__(self):
        if self.sib_sp < 0 or self.parch < 0:
            raise ValueError("가족 수는 음수일 수 없습니다.")
            
    @property
    def total_on_board(self) -> int:
        return self.sib_sp + self.parch