"""Base.metadata 에 ORM 클래스를 등록합니다. database.init_db() 직전에 한 번 호출합니다."""


def import_all_models() -> None:
    from domain_intake.models.faq_entry import FaqEntry  # noqa: F401
    from domain_intake.models.gallery_item import GalleryItem  # noqa: F401
    from domain_intake.models.library_item import LibraryItem  # noqa: F401
    from domain_intake.models.magazine_article import MagazineArticle  # noqa: F401
    from domain_intake.models.studio_analytics import StudioAnalytics  # noqa: F401
    from domain_intake.models.studio_workspace import StudioWorkspace  # noqa: F401
    from secom.app.models.user import User  # noqa: F401
    from titanic.app.use_cases.passenger import Passenger  # noqa: F401
    from ml_data.models.audio_features import AudioFeature  # noqa: F401
    from ml_data.models.generation_logs import GenerationLog  # noqa: F401
    from ml_data.models.user_events import UserEvent  # noqa: F401
    from ml_data.models.visual_ratings import VisualRating  # noqa: F401

