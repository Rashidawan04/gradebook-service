
import gradebook


def test_student_with_no_marks_gets_zero(monkeypatch):
    state = {
        "students": {
            "S1": {"id": "S1", "name": "Ayesha"}
        },
        "assessments": {},
        "marks": [],
    }

    monkeypatch.setattr(gradebook, "STATE", state)

    result = gradebook.pct("S1")

    assert result == "0"


def test_student_with_one_mark_gets_percentage(monkeypatch):
    state = {
        "students": {
            "S1": {"id": "S1", "name": "Ayesha"}
        },
        "assessments": {
            "A1": {
                "id": "A1",
                "name": "Quiz",
                "weight": 10,
                "total": 20,
            }
        },
        "marks": [
            {"student": "S1", "assessment": "A1", "score": 15}
        ],
    }

    monkeypatch.setattr(gradebook, "STATE", state)

    result = gradebook.pct("S1")

    assert result == "7.5"


def test_mark_for_nonexistent_assessment_is_ignored(monkeypatch):
    state = {
        "students": {
            "S1": {"id": "S1", "name": "Ayesha"}
        },
        "assessments": {},
        "marks": [
            {"student": "S1", "assessment": "A99", "score": 15}
        ],
    }

    monkeypatch.setattr(gradebook, "STATE", state)

    result = gradebook.pct("S1")

    assert result == "0"