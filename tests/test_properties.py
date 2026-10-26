
from unittest.mock import patch

from hypothesis import given
from hypothesis import strategies as st

import gradebook
from models import parse_mark


@given(
    scores=st.lists(
        st.integers(min_value=0, max_value=20),
        min_size=1,
        max_size=5,
    )
)
def test_pct_does_not_overcount_duplicate_marks(scores):
    state = {
        "students": {
            "S1": {"id": "S1", "name": "Ayesha"},
        },
        "assessments": {
            "A1": {
                "id": "A1",
                "title": "Quiz 1",
                "weight": "10",
                "total": "20",
            },
        },
        "marks": [],
    }

    def save():
        pass

    for score in scores:
        mark = parse_mark(
            {
                "student": "S1",
                "assessment": "A1",
                "score": score,
            }
        )
        gradebook.add_mark(
            state,
            mark,
            lambda: "2026-10-12 09:00:00",
            save,
        )

    with patch.object(gradebook, "STATE", state):
        assert float(gradebook.pct("S1")) <= 10
