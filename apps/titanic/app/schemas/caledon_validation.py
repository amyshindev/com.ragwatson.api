from typing import Any, Dict

from titanic.app.schemas.passenger_schema import PassengerSchema


class CaledonValidation:
    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_passenger(data: Dict[str, Any]) -> bool:
        """Validate passenger data using PassengerSchema."""
        try:
            PassengerSchema(**data)
            return True
        except Exception:
            return False
