from pydantic import BaseModel, Field


class CrewJamesDirectorSchema(BaseModel):
    """Titanic passenger upload row (James CSV upload)."""

    passenger_id: str | None = Field(None, description="Passenger id")
    survived: str | None = Field(None, description="Survived flag")
    pclass: str | None = Field(None, description="Ticket class")
    name: str | None = Field(None, description="Passenger name")
    gender: str | None = Field(None, description="Gender (male / female)")
    age: str | None = Field(None, description="Age")
    sibsp: str | None = Field(None, description="Siblings/spouses aboard")
    parch: str | None = Field(None, description="Parents/children aboard")
    ticket: str | None = Field(None, description="Ticket number")
    fare: str | None = Field(None, description="Fare")
    cabin: str | None = Field(None, description="Cabin")
    embarked: str | None = Field(None, description="Embarkation port")
