"""Base.metadata 에 ORM 클래스를 등록합니다. database.init_db() 직전에 한 번 호출합니다."""


def import_all_models() -> None:
    from domain_intake.models.domain_intake_record import DomainIntakeRecord  # noqa: F401
    from secom.app.models.user import User  # noqa: F401
