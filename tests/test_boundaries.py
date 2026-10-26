
import pytest

import gradebook
from errors import ValidationError
from models import Assessment, parse_mark


@pytest.mark.parametrize(
    "weight",
    [0, 100],
    ids=["weight-zero", "weight-one-hundred"],
)
def test_assessment_accepts_boundary_weights(weight):
    assessment = Assessment(
        id="A1",
        title="Quiz",
        weight=weight,
        total=20,
    )
    assert assessment.weight == weight


@pytest.mark.parametrize(
    "weight",
    [-0.01, 100.01],
    ids=["weight-below-zero", "weight-above-one-hundred"],
)
def test_assessment_rejects_out_of_range_weights(weight):
    with pytest.raises(ValidationError):
        Assessment(
            id="A1",
            title="Quiz",
            weight=weight,
            total=20,
        )


def test_assessment_accepts_total_point_zero_one():
    assessment = Assessment(
        id="A1",
        title="Quiz",
        weight=10,
        total=0.01,
    )
    assert assessment.total == 0.01


def test_assessment_rejects_total_zero():
    with pytest.raises(ValidationError):
        Assessment(
            id="A1",
            title="Quiz",
            weight=10,
            total=0,
        )


@pytest.mark.parametrize(
    "score",
    [0, 20],
    ids=["score-zero", "score-equals-total"],
)
def test_add_mark_accepts_boundary_scores(loaded, score):
    saved = []

    def save():
        saved.append(True)

    mark = parse_mark(
        {
            "student": "S1",
            "assessment": "A1",
            "score": score,
        }
    )

    gradebook.add_mark(
        loaded,
        mark,
        lambda: "2026-10-12 09:00:00",
        save,
    )

    assert len(loaded["marks"]) == 1
    assert float(loaded["marks"][0]["score"]) == score
    assert saved == [True]


@pytest.mark.parametrize(
    "score",
    [-0.01, 20.01],
    ids=["score-below-zero", "score-above-total"],
)
def test_add_mark_rejects_out_of_range_scores(loaded, score):
    saved = []

    def save():
        saved.append(True)

    with pytest.raises(ValidationError):
        mark = parse_mark(
            {
                "student": "S1",
                "assessment": "A1",
                "score": score,
            }
        )

        gradebook.add_mark(
            loaded,
            mark,
            lambda: "2026-10-12 09:00:00",
            save,
        )

    assert loaded["marks"] == []
    assert saved == []
