from typing import Any

from titanic.adapter.inbound.api.schemas.james_schema import JamesSchema


class CaledonValidation:
    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_passenger(data: dict[str, Any]) -> bool:
        """Validate passenger data using JamesSchema."""
        try:
            JamesSchema.model_validate(data)
            return True
        except Exception:
            return False
