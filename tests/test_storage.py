
import json

import pytest

import gradebook


@pytest.fixture
def data_file(tmp_path, monkeypatch):
    path = tmp_path / "gradebook.json"
    monkeypatch.setattr(gradebook, "DATA", str(path))
    return path


def test_save_and_load_preserves_gradebook(data_file, monkeypatch):
    original_state = {
        "students": {
            "S1": {"id": "S1", "name": "Ayesha"}
        },
        "assessments": {
            "A1": {
                "id": "A1",
                "title": "Quiz",
                "weight": "20",
                "total": "50"
            }
        },
        "marks": [
            {
                "student": "S1",
                "assessment": "A1",
                "score": "15",
                "at": "2026-10-12 09:00:00"
            }
        ]
    }

    monkeypatch.setattr(gradebook, "STATE", original_state)

    gradebook.save()

    monkeypatch.setattr(gradebook, "STATE", {})
    gradebook.load()

    assert gradebook.STATE == original_state


def test_load_missing_file_creates_empty_state(data_file):
    gradebook.load()

    assert gradebook.STATE == {
        "students": {},
        "assessments": {},
        "marks": []
    }


def test_load_invalid_json_raises_error(data_file):
    data_file.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        gradebook.load()
