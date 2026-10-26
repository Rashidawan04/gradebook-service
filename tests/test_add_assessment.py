
import pytest

from errors import ConflictError, ValidationError
from gradebook import add_assessment
from models import Assessment


def test_add_assessment_saves_valid_assessment():
    state = {
        "students": {},
        "assessments": {},
        "marks": [],
    }
    assessment = Assessment(
        id="a1",
        title="Quiz",
        weight=40.0,
        total=20.0,
    )
    saved = []

    def save():
        saved.append(True)

    add_assessment(state, assessment, save)

    assert "a1" in state["assessments"]
    assert state["assessments"]["a1"]["title"] == "Quiz"
    assert len(saved) == 1


def test_add_assessment_rejects_weight_over_100():
    state = {
        "students": {},
        "assessments": {
            "a1": {
                "id": "a1",
                "title": "Quiz",
                "weight": "60",
                "total": "20",
            }
        },
        "marks": [],
    }
    assessment = Assessment(
        id="a2",
        title="Exam",
        weight=50.0,
        total=100.0,
    )
    saved = []

    def save():
        saved.append(True)

    with pytest.raises(ValidationError, match="100"):
        add_assessment(state, assessment, save)

    assert "a2" not in state["assessments"]
    assert saved == []


def test_add_assessment_rejects_duplicate_id():
    state = {
        "students": {},
        "assessments": {
            "a1": {
                "id": "a1",
                "title": "Quiz",
                "weight": "40",
                "total": "20",
            }
        },
        "marks": [],
    }
    assessment = Assessment(
        id="a1",
        title="Another Quiz",
        weight=20.0,
        total=10.0,
    )
    saved = []

    def save():
        saved.append(True)

    with pytest.raises(ConflictError, match="already exists"):
        add_assessment(state, assessment, save)

    assert state["assessments"]["a1"]["title"] == "Quiz"
    assert saved == []
