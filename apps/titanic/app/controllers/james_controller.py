from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.services.jack_service import JackService

app = FastAPI(title="Titanic (James)")


class JamesController:
    def __init__(self, session: AsyncSession | None = None) -> None:
        self.service = JackService(session)

    def get_data(self):
        """Synchronously retrieves data (first row from CSV)."""
        return self.service.get_data()

    async def get_data_db(self):
        """Asynchronously retrieves data from DB or CSV fallback."""
        return await self.service.get_data_db()

    def get_count(self):
        """Synchronously retrieves count."""
        return self.service.get_count()

    async def get_count_db(self):
        """Asynchronously retrieves count from DB or CSV fallback."""
        return await self.service.get_count_db()

    def has_decision_tree_model(self) -> bool:
        """Checks if decision tree model file exists."""
        return self.service.has_decision_tree_model()

    def get_model_name_and_accuracy(self):
        """Retrieves model metadata."""
        return self.service.get_model_name_and_accuracy()
