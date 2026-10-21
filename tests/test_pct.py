
import gradebook


def test_student_with_no_marks_gets_zero(loaded):
    result = gradebook.pct("S1")
    assert result == "0"


def test_student_with_one_quiz_mark_gets_seven_point_five(loaded):
    loaded["marks"].append({
        "student": "S1",
        "assessment": "A1",
        "score": "15",
        "at": "2026-10-12 09:00:00"
    })

    result = gradebook.pct("S1")
    assert result == "7.5"


def test_mark_for_missing_assessment_is_ignored(loaded):
    loaded["marks"].append({
        "student": "S1",
        "assessment": "UNKNOWN",
        "score": "15",
        "at": "2026-10-12 09:00:00"
    })

    result = gradebook.pct("S1")
    assert result == "0"
