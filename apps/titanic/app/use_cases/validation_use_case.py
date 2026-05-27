from typing import Any

from titanic.app.schemas.passenger_schema import PassengerSchema


class CaledonValidation:
    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_passenger(data: dict[str, Any]) -> bool:
        """Validate passenger data using PassengerSchema."""
        try:
            PassengerSchema(**data)
            return True
        except Exception:
            return False
