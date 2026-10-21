import pytest

from errors import ValidationError
from models import (
    Assessment,
    parse_assessment,
    parse_mark,
    parse_number,
    parse_student,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("15", 15.0, id="integer-string"),
        pytest.param(15, 15.0, id="integer"),
        pytest.param("2.5", 2.5, id="decimal-string"),
    ],
)
def test_good_numbers_are_accepted(
    value: object, expected: float
) -> None:
    assert parse_number(value, "score") == expected


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("abc", id="text"),
        pytest.param(True, id="boolean"),
        pytest.param(None, id="none"),
        pytest.param([], id="list"),
        pytest.param("nan", id="nan"),
        pytest.param("inf", id="infinity"),
    ],
)
def test_bad_numbers_are_rejected(value: object) -> None:
    with pytest.raises(ValidationError):
        parse_number(value, "score")


def test_zero_assessment_total_is_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_assessment(
            {
                "id": "A1",
                "title": "Quiz",
                "weight": 20,
                "total": 0,
            }
        )


def test_negative_score_is_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_mark(
            {
                "student": "S1",
                "assessment": "A1",
                "score": -1,
            }
        )


def test_missing_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_student({"id": "S1"})


def test_non_dict_payload_is_rejected() -> None:
    with pytest.raises(ValidationError):
        parse_student(["S1", "Alice"])


def test_valid_assessment_is_parsed_correctly() -> None:
    result = parse_assessment(
        {
            "id": "A1",
            "title": "Quiz",
            "weight": "20",
            "total": "50",
        }
    )

    assert result == Assessment(
        id="A1",
        title="Quiz",
        weight=20.0,
        total=50.0,
    )