from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.models.rose_model import RoseModel, model_file_exists
from titanic.app.use_cases.walter_reader import WalterReader


class JackService:
    def __init__(self, session: AsyncSession | None = None) -> None:
        self.walter = WalterReader(session)
        self.rose = RoseModel()

    async def get_data_db(self):
        """Asynchronously retrieves Titanic data from DB."""
        return await self.walter.get_data_db()

    async def get_count_db(self) -> int:
        """Asynchronously retrieves passenger count from DB."""
        return await self.walter.get_count_db()

    def has_decision_tree_model(self) -> bool:
        """Checks if the decision tree model file exists."""
        return model_file_exists()

    def get_model_name_and_accuracy(self) -> str:
        """Retrieves the model name."""
        return self.rose.get_model_name()
