import pytest

from titanic.domain.value_objects.age_vo import Age
from titanic.domain.value_objects.gender_vo import Gender, GenderType
from titanic.domain.value_objects.name_vo import Name
from titanic.domain.value_objects.parch_vo import Parch
from titanic.domain.value_objects.sib_sp_vo import SibSp
from titanic.domain.value_objects.survived_vo import Survived
from titanic.domain.value_objects.title_vo import Title


class TestTitle:
    def test_from_name_mr(self):
        assert Title.from_name("Braund, Mr. Owen").nominal_code == 1

    def test_from_name_miss(self):
        assert Title.from_name("Cumings, Mrs. John Bradley").nominal_code == 3

    def test_from_name_master(self):
        assert Title.from_name("Palsson, Master. Gosta").nominal_code == 4

    def test_rare_title_maps_to_rare_code(self):
        assert Title.from_name("McCarthy, Rev. Timothy").nominal_code == 6

    def test_royal_title_maps_to_royal_code(self):
        assert Title.from_name("Fortune, Miss. Mabel").nominal_code == 2
        assert Title.from_raw("Lady").nominal_code == 5

    def test_ms_alias_maps_like_reference(self):
        assert Title.from_raw("Ms").nominal_code == 2

    def test_mlle_alias_maps_like_reference(self):
        assert Title.from_raw("Mlle").nominal_code == 1

    def test_missing_title_returns_unknown_code(self):
        assert Title.from_name("NoTitle Here").nominal_code == 0


class TestName:
    def test_valid_name_creates_successfully(self):
        name = Name("Dawson, Mr. Jack")
        assert name.value == "Dawson, Mr. Jack"

    def test_empty_string_raises(self):
        with pytest.raises(ValueError):
            Name("")

    def test_exactly_200_chars_is_allowed(self):
        Name("A" * 200)

    def test_201_chars_raises(self):
        with pytest.raises(ValueError, match="200자"):
            Name("A" * 201)

    def test_normalized_strips_surrounding_whitespace(self):
        assert Name("  Jack  ").normalized == "Jack"


class TestGender:
    def test_from_raw_male(self):
        assert Gender.from_raw("male").value == GenderType.MALE

    def test_from_raw_female(self):
        assert Gender.from_raw("female").value == GenderType.FEMALE

    def test_from_raw_none_is_unknown(self):
        assert Gender.from_raw(None).value == GenderType.UNKNOWN

    def test_from_raw_uppercase_is_normalized(self):
        assert Gender.from_raw("MALE").value == GenderType.MALE

    def test_from_raw_unrecognized_string_is_unknown(self):
        assert Gender.from_raw("other").value == GenderType.UNKNOWN

    def test_is_female_true_for_female(self):
        assert Gender.from_raw("female").is_female() is True

    def test_is_female_false_for_male(self):
        assert Gender.from_raw("male").is_female() is False

    def test_is_female_false_for_unknown(self):
        assert Gender.from_raw(None).is_female() is False


class TestAge:
    def test_from_raw_valid_string(self):
        assert Age.from_raw("22.5").value == 22.5

    def test_from_raw_none_is_unknown(self):
        assert Age.from_raw(None).is_unknown is True

    def test_from_raw_empty_string_is_unknown(self):
        assert Age.from_raw("").is_unknown is True

    def test_negative_age_raises(self):
        with pytest.raises(ValueError):
            Age(value=-1.0)

    def test_age_over_120_raises(self):
        with pytest.raises(ValueError):
            Age(value=121.0)

    def test_boundary_0_is_valid(self):
        Age(value=0.0)

    def test_boundary_120_is_valid(self):
        Age(value=120.0)

    def test_non_numeric_string_raises(self):
        with pytest.raises(ValueError, match="유효하지 않은"):
            Age.from_raw("abc")

    def test_is_minor_true_under_18(self):
        assert Age(value=17.9).is_minor is True

    def test_is_minor_false_at_18(self):
        assert Age(value=18.0).is_minor is False

    def test_is_minor_false_for_unknown_age(self):
        assert Age(value=None).is_minor is False


class TestSibSp:
    def test_from_raw_parses_string_values(self):
        assert SibSp.from_raw("1").value == 1

    def test_from_raw_none_defaults_to_zero(self):
        assert SibSp.from_raw(None).value == 0

    def test_has_sibling_or_spouse(self):
        assert SibSp(value=1).has_sibling_or_spouse is True
        assert SibSp(value=0).has_sibling_or_spouse is False

    def test_negative_value_raises(self):
        with pytest.raises(ValueError, match="SibSp"):
            SibSp(value=-1)


class TestParch:
    def test_from_raw_parses_string_values(self):
        assert Parch.from_raw("2").value == 2

    def test_from_raw_none_defaults_to_zero(self):
        assert Parch.from_raw(None).value == 0

    def test_has_parent_or_child(self):
        assert Parch(value=1).has_parent_or_child is True
        assert Parch(value=0).has_parent_or_child is False

    def test_negative_value_raises(self):
        with pytest.raises(ValueError, match="Parch"):
            Parch(value=-1)


class TestSurvived:
    def test_from_raw_1_means_survived(self):
        assert Survived.from_raw("1").survived is True

    def test_from_raw_0_means_did_not_survive(self):
        assert Survived.from_raw("0").survived is False

    def test_from_raw_none_is_unknown(self):
        assert Survived.from_raw(None).is_unknown is True

    def test_from_raw_empty_string_is_unknown(self):
        assert Survived.from_raw("").is_unknown is True

    def test_from_raw_invalid_value_raises(self):
        with pytest.raises(ValueError, match="유효하지 않은"):
            Survived.from_raw("2")

    def test_is_unknown_false_when_survival_is_known(self):
        assert Survived.from_raw("1").is_unknown is False
