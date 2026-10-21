
from unittest.mock import Mock

import pytest

import gradebook
from errors import NotFoundError, ValidationError
from models import parse_mark


def fixed_clock() -> str:
    """Stub that always returns the same timestamp."""
    return "2026-10-12 09:00:00"


def test_valid_mark_is_stored_with_expected_time(loaded):
    save = Mock()

    mark = parse_mark(
        {
            "student": "S1",
            "assessment": "A1",
            "score": "15",
        }
    )

    gradebook.add_mark(loaded, mark, fixed_clock, save)

    assert loaded["marks"] == [
        {
            "student": "S1",
            "assessment": "A1",
            "score": "15.0",
            "at": "2026-10-12 09:00:00",
        }
    ]


def test_valid_mark_calls_save_once(loaded):
    save = Mock()

    mark = parse_mark(
        {
            "student": "S1",
            "assessment": "A1",
            "score": "15",
        }
    )

    gradebook.add_mark(loaded, mark, fixed_clock, save)

    save.assert_called_once_with()


@pytest.mark.parametrize(
    ("data", "exception"),
    [
        pytest.param(
            {
                "student": "UNKNOWN",
                "assessment": "A1",
                "score": "15",
            },
            NotFoundError,
            id="unknown-student",
        ),
        pytest.param(
            {
                "student": "S1",
                "assessment": "UNKNOWN",
                "score": "15",
            },
            NotFoundError,
            id="unknown-assessment",
        ),
        pytest.param(
            {
                "student": "S1",
                "assessment": "A1",
                "score": "21",
            },
            ValidationError,
            id="score-above-total",
        ),
    ],
)
def test_invalid_mark_changes_nothing_and_does_not_save(
    loaded, data, exception
):
    save = Mock()
    mark = parse_mark(data)

    with pytest.raises(exception):
        gradebook.add_mark(loaded, mark, fixed_clock, save)

    assert loaded["marks"] == []
    save.assert_not_called()
