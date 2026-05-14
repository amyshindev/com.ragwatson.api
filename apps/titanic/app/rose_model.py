from pathlib import Path

from sklearn.tree import DecisionTreeClassifier

_DATA_DIR = Path(__file__).resolve().parent
_JOBLIB_PATH = _DATA_DIR / "titanic_decision_tree.joblib"
_MODEL_PATH = _JOBLIB_PATH


def model_file_exists() -> bool:
    return _MODEL_PATH.is_file()


class RoseModel:
    def __init__(self) -> None:
        self.model = DecisionTreeClassifier()

    def get_model_name(self) -> str:
        return type(self.model).__name__