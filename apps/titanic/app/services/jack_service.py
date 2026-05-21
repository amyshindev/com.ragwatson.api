from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.models.rose_model import RoseModel, model_file_exists
from titanic.app.repositories.walter_reader import WalterReader


class JackService:
    def __init__(self, session: AsyncSession | None = None) -> None:
        self.walter = WalterReader(session)
        self.rose = RoseModel()

    def get_data(self):
        """Synchronously retrieves data from CSV."""
        return self.walter.get_data()

    async def get_data_db(self):
        """Asynchronously retrieves data from DB (or CSV fallback)."""
        return await self.walter.get_data_db()

    def get_count(self):
        """Synchronously retrieves passenger count from CSV."""
        return self.walter.get_count()

    async def get_count_db(self):
        """Asynchronously retrieves passenger count from DB (or CSV fallback)."""
        return await self.walter.get_count_db()

    def has_decision_tree_model(self) -> bool:
        """Checks if the decision tree model file exists."""
        return model_file_exists()

    def get_model_name_and_accuracy(self):
        """Retrieves the model name."""
        return self.rose.get_model_name()
