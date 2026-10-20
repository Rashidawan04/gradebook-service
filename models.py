
import math
from dataclasses import dataclass

from errors import ValidationError


def parse_number(raw: object, field: str) -> float:
    if isinstance(raw, bool):
        raise ValidationError(f"{field} must be a number")

    if isinstance(raw, (int, float)):
        value = float(raw)
    elif isinstance(raw, str):
        try:
            value = float(raw.strip())
        except ValueError:
            raise ValidationError(
                f"{field} must be a number"
            ) from None
    else:
        raise ValidationError(f"{field} must be a number")

    if not math.isfinite(value):
        raise ValidationError(f"{field} must be finite")

    return value


def parse_text(raw: object, field: str) -> str:
    if not isinstance(raw, str):
        raise ValidationError(f"{field} must be a string")

    value = raw.strip()

    if not value:
        raise ValidationError(f"{field} must not be blank")

    return value


@dataclass(frozen=True)
class Student:
    id: str
    name: str

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValidationError("id must not be empty")
        if not self.name.strip():
            raise ValidationError("name must not be empty")


@dataclass(frozen=True)
class Assessment:
    id: str
    title: str
    weight: float
    total: float

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValidationError("id must not be empty")
        if not self.title.strip():
            raise ValidationError("title must not be empty")
        if not 0 <= self.weight <= 100:
            raise ValidationError("weight must be between 0 and 100")
        if self.total <= 0:
            raise ValidationError("total must be above 0")


@dataclass(frozen=True)
class Mark:
    student: str
    assessment: str
    score: float

    def __post_init__(self) -> None:
        if not self.student.strip():
            raise ValidationError("student must not be empty")
        if not self.assessment.strip():
            raise ValidationError("assessment must not be empty")
        if self.score < 0:
            raise ValidationError("score must not be negative")


def _payload(payload: object) -> dict[str, object]:
    if not isinstance(payload, dict):
        raise ValidationError("body must be a JSON object")

    if not all(isinstance(key, str) for key in payload):
        raise ValidationError("JSON object keys must be strings")

    return payload


def _required(data: dict[str, object], field: str) -> object:
    if field not in data:
        raise ValidationError(f"{field} is required")

    return data[field]


def parse_student(payload: object) -> Student:
    data = _payload(payload)

    return Student(
        id=parse_text(_required(data, "id"), "id"),
        name=parse_text(_required(data, "name"), "name"),
    )


def parse_assessment(payload: object) -> Assessment:
    data = _payload(payload)

    return Assessment(
        id=parse_text(_required(data, "id"), "id"),
        title=parse_text(_required(data, "title"), "title"),
        weight=parse_number(_required(data, "weight"), "weight"),
        total=parse_number(_required(data, "total"), "total"),
    )


def parse_mark(payload: object) -> Mark:
    data = _payload(payload)

    return Mark(
        student=parse_text(_required(data, "student"), "student"),
        assessment=parse_text(
            _required(data, "assessment"), "assessment"
        ),
        score=parse_number(_required(data, "score"), "score"),
    )
