
import pytest

import gradebook


@pytest.mark.parametrize(
    ("marks", "expected"),
    [
        pytest.param([], "0", id="no-marks"),
        pytest.param(
            [{"student": "S1", "assessment": "A1",
              "score": "15", "at": "2026-10-12 09:00:00"}],
            "7.5",
            id="quiz-score-15"
        ),
        pytest.param(
            [{"student": "S1", "assessment": "A1",
              "score": "20", "at": "2026-10-12 09:00:00"}],
            "10.0",
            id="quiz-full-marks"
        ),
        pytest.param(
            [{"student": "S1", "assessment": "A1",
              "score": "0", "at": "2026-10-12 09:00:00"}],
            "0.0",
            id="zero-score"
        ),
        pytest.param(
            [
                {"student": "S1", "assessment": "A1",
                 "score": "15", "at": "2026-10-12 09:00:00"},
                {"student": "S1", "assessment": "A2",
                 "score": "40", "at": "2026-10-12 09:00:00"}
            ],
            "31.5",
            id="two-assessments"
        )
    ]
)
def test_percentage_for_different_marks(loaded, marks, expected):
    loaded["marks"] = marks
    result = gradebook.pct("S1")
    assert result == expected
