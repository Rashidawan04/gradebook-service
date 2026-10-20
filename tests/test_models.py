
import math

import pytest

from errors import ValidationError
from models import (
    Assessment,
    parse_assessment,
    parse_mark,
    parse_number,
    parse_student,
)


def test_numeric_string_is_accepted() -> None:
    assert parse_number("12.5", "score") == 12.5


@pytest.mark.parametrize(
    "value",
    ["text", True, math.nan],
)
def test_text_bool_and_nan_are_rejected(value: object) -> None:
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
