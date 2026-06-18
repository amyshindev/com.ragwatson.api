from titanic.domain.value_objects.age_vo import Age
from titanic.domain.value_objects.cabin_vo import Cabin
from titanic.domain.value_objects.embarked_vo import Embarked, EmbarkedType
from titanic.domain.value_objects.fare_vo import Fare
from titanic.domain.value_objects.gender_vo import Gender, GenderType
from titanic.domain.value_objects.name_vo import Name
from titanic.domain.value_objects.parch_vo import Parch
from titanic.domain.value_objects.pclass_vo import PClass, PClassType
from titanic.domain.value_objects.sib_sp_vo import SibSp
from titanic.domain.value_objects.survived_vo import Survived, SurvivedType
from titanic.domain.value_objects.ticket_vo import Ticket
from titanic.domain.value_objects.title_vo import Title, TitleCategory

# Backward-compatible aliases
PassengerName = Name
SurvivalStatus = Survived

__all__ = [
    "Age",
    "Cabin",
    "Embarked",
    "EmbarkedType",
    "Fare",
    "Gender",
    "GenderType",
    "Name",
    "Parch",
    "PassengerName",
    "PClass",
    "PClassType",
    "SibSp",
    "Survived",
    "SurvivedType",
    "SurvivalStatus",
    "Ticket",
    "Title",
    "TitleCategory",
]
