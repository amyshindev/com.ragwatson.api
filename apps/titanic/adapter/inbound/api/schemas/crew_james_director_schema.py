from typing import Optional

from pydantic import BaseModel, Field


class CrewJamesDirectorSchema(BaseModel):
    """Titanic passenger upload row (James CSV upload)."""

    passenger_id: Optional[str] = Field(None, description="Passenger id")
    survived: Optional[str] = Field(None, description="Survived flag")
    pclass: Optional[str] = Field(None, description="Ticket class")
    name: Optional[str] = Field(None, description="Passenger name")
    gender: Optional[str] = Field(None, description="Gender (male / female)")
    age: Optional[str] = Field(None, description="Age")
    sibsp: Optional[str] = Field(None, description="Siblings/spouses aboard")
    parch: Optional[str] = Field(None, description="Parents/children aboard")
    ticket: Optional[str] = Field(None, description="Ticket number")
    fare: Optional[str] = Field(None, description="Fare")
    cabin: Optional[str] = Field(None, description="Cabin")
    embarked: Optional[str] = Field(None, description="Embarkation port")
