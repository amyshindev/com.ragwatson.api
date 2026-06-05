"""Base.metadata 에 ORM 클래스를 등록합니다. database.init_db() 직전에 한 번 호출합니다."""


def import_all_models() -> None:
    from domain_intake.models.faq_entry import FaqEntry  # noqa: F401
    from domain_intake.models.gallery_item import GalleryItem  # noqa: F401
    from domain_intake.models.genre import Genre, GalleryItemGenre  # noqa: F401
    from domain_intake.models.library_item import LibraryItem  # noqa: F401
    from domain_intake.models.magazine_article import MagazineArticle  # noqa: F401
    from domain_intake.models.platform_spec import PlatformSpec  # noqa: F401
    from domain_intake.models.studio_analytics import StudioAnalytics  # noqa: F401
    from domain_intake.models.studio_workspace import StudioWorkspace  # noqa: F401
    from domain_intake.models.style_tag import StyleTag, WorkspaceStyleTag  # noqa: F401
    from friday13th.adapter.outbound.orm.admin_model import AdminRecord  # noqa: F401
    from friday13th.adapter.outbound.orm.friday13th_model import UserRecord  # noqa: F401
    from titanic.adapter.outbound.orm.booking_orm import BookingOrm  # noqa: F401
    from titanic.adapter.outbound.orm.person_orm import PersonOrm  # noqa: F401
    from ml_data.adapter.outbound.orm.audio_feature_orm import AudioFeature  # noqa: F401
    from ml_data.adapter.outbound.orm.generation_log_orm import GenerationLog  # noqa: F401
    from ml_data.adapter.outbound.orm.user_event_orm import UserEvent  # noqa: F401
    from ml_data.adapter.outbound.orm.visual_rating_orm import VisualRating  # noqa: F401
