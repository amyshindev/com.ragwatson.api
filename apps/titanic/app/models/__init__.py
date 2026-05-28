"""하위 호환: ORM·모델은 ``titanic.app.use_cases`` 로 이동했습니다."""

from titanic.app.use_cases.passenger import Passenger
from titanic.app.use_cases.rose_model import RoseModel, model_file_exists

__all__ = ["Passenger", "RoseModel", "model_file_exists"]
