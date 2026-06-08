import logging

_LOG_SEP = "#" * 56
_LOG_STEP = "1\uFE0F\u20E3"

_CHARACTER_LABELS: dict[str, str] = {
    "CrewWalterRoasterRouter": "\uc6d4\ud130",
    "CrewAndrewsArchitectRouter": "\uc565\ub4dc\ub968\uc2a4",
    "CrewHartleyViolinRouter": "\ud558\ud2c0\ub9ac",
    "CrewLoweBoatRouter": "\ub85c\uc6b0",
    "CrewSmithCaptainRouter": "\uc2a4\ubbf8\uc2a4",
    "PassengerCalTesterRouter": "\uce98\ub7ec\ub4e0",
    "PassengerIsidorCoupleRouter": "\uc774\uc2dc\ub3c4\ub974",
    "PassengerJackTrainerRouter": "\uc7ad",
    "PassengerMollyScalerRouter": "\ubaac\ub9ac",
    "PassengerRoseModelRouter": "\ub85c\uc988",
    "PassengerRuthValidationRouter": "\ub8e8\uc2a4",
}


def log_myself_intro(
    log: logging.Logger,
    router_name: str,
    schema_id: int,
    schema_name: str,
) -> None:
    character = _CHARACTER_LABELS.get(router_name, schema_name)
    intro = (
        f"{_LOG_STEP}  [{router_name}] "
        f"schema\uc5d0\uc11c \uac00\uc838\uc628 {character} \uc790\uae30\uc18c\uac1c\uae00"
    )
    log.info(_LOG_SEP)
    log.info(intro)
    log.info("%s  ID: %s", _LOG_STEP, schema_id)
    log.info("%s  NAME: %s", _LOG_STEP, schema_name)
    log.info(_LOG_SEP)
