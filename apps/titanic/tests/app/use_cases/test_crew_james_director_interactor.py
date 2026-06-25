from unittest.mock import AsyncMock, MagicMock

import pytest

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import CrewJamesDirectorSchema
from titanic.app.use_cases.crew_james_director_interactor import JamesDirectorInteractor


@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.receive_uploaded_records = AsyncMock(return_value=3)
    return repo


@pytest.fixture
def mock_session():
    session = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    return session


@pytest.fixture
def interactor(mock_session, mock_repository):
    return JamesDirectorInteractor(session=mock_session, repository=mock_repository)


def _schema(**overrides) -> CrewJamesDirectorSchema:
    defaults = {
        "passenger_id": "1",
        "survived": "0",
        "pclass": "3",
        "name": "Braund, Mr. Owen",
        "gender": "male",
        "age": "22",
        "sibsp": "1",
        "parch": "0",
        "ticket": "A/5 21171",
        "fare": "7.25",
        "cabin": None,
        "embarked": "S",
    }
    defaults.update(overrides)
    return CrewJamesDirectorSchema(**defaults)


class TestUploadTitanicFile:
    async def test_creates_one_passenger_command_per_record(self, interactor, mock_repository):
        await interactor.upload_titanic_file([_schema(passenger_id="1"), _schema(passenger_id="2")])

        person_commands, _ = mock_repository.receive_uploaded_records.call_args.args
        assert len(person_commands) == 2

    async def test_passenger_command_contains_correct_fields(self, interactor, mock_repository):
        await interactor.upload_titanic_file([_schema(passenger_id="7", gender="female", age="28")])

        person_commands, _ = mock_repository.receive_uploaded_records.call_args.args
        cmd = person_commands[0]
        assert cmd.passenger_id == "7"
        assert cmd.gender == "female"
        assert cmd.age == "28"

    async def test_booking_command_contains_correct_fields(self, interactor, mock_repository):
        await interactor.upload_titanic_file([_schema(pclass="1", fare="100.0", embarked="C")])

        _, booking_commands = mock_repository.receive_uploaded_records.call_args.args
        cmd = booking_commands[0]
        assert cmd.pclass == "1"
        assert cmd.fare == "100.0"
        assert cmd.embarked == "C"

    async def test_none_fields_become_empty_string(self, interactor, mock_repository):
        await interactor.upload_titanic_file([_schema(survived=None, cabin=None)])

        person_commands, booking_commands = mock_repository.receive_uploaded_records.call_args.args
        assert person_commands[0].survived == ""
        assert booking_commands[0].cabin == ""

    async def test_returns_saved_count_from_repository(self, interactor, mock_session):
        result = await interactor.upload_titanic_file([_schema()])

        assert result == {"saved": 3}
        mock_session.commit.assert_awaited_once()
