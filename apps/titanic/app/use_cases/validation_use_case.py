from typing import Any

from titanic.adapter.inbound.api.schemas.james_schema import JamesPassengerRow


class CaledonValidation:
    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_passenger(data: dict[str, Any]) -> bool:
        """Validate passenger data using JamesPassengerRow."""
        try:
            JamesPassengerRow.from_payload(data)
            return True
        except Exception:
            return False
