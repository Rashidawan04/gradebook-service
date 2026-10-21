# Task 2 - Failing Well

## (a) GET /students/NOPE

Command:

curl.exe -i http://localhost:8000/students/NOPE

Result:

HTTP 200 with {"error":"not found"}

Expected after fixing:

HTTP 404


## (b) POST /students with body 5

Command:

curl.exe -i -X POST http://localhost:8000/students -d "5"

Result:

No proper HTTP response / server traceback.

Expected after fixing:

HTTP 400


## (c) Invalid score "abc"

Commands:

curl.exe -i -X POST http://localhost:8000/students -d '{"id":"S1","name":"Ayesha"}'

curl.exe -i -X POST http://localhost:8000/assessments -d '{"id":"A1","title":"Quiz 1","weight":"10","total":"20"}'

curl.exe -i -X POST http://localhost:8000/marks -d '{"student":"S1","assessment":"A1","score":"abc"}'

curl.exe -i http://localhost:8000/students/S1

Result:

The invalid score is accepted with HTTP 200. Later percentage calculation
causes a ValueError because "abc" cannot be converted to float.


## (d) Assessment total "0"

Result:

The old service accepts total 0 and later crashes with ZeroDivisionError
when calculating the report.


## (e) Mark for nonexistent assessment

Test: POST a mark for student `S1` with assessment `NOPE`.

Actual result:

HTTP/1.0 404 Not Found

{"error": "assessment not found"}

Observation: The service rejected the mark because the assessment does not exist and returned HTTP 404.



## Why gradebook.json was deleted

gradebook.json was deleted to reset the persistent state of the service.
This ensured that each experiment started with clean data.


## Bare except locations

The bare except statements were found at:

- Line 18
- Line 26
- Line 79


## Task 8 — Model Tests

Command: `python -m pytest -q`

Result: 8 passed

### Static checks

- `python -m mypy gradebook.py` — passed
- `python -m mypy --strict errors.py models.py` — passed
- `ruff check .` — passed


# Lab 04 Notes

## Task 8: Demonstrating Test Failure

I temporarily changed the percentage calculation in `pct()`
from division to multiplication.

This caused percentage tests to fail, demonstrating that the
tests detect incorrect calculation logic.

After restoring the correct division operator, the tests passed
again.

## Test Doubles

- Stub: `fixed_clock()` returns a fixed timestamp.
- Fake: The `loaded` fixture supplies in-memory gradebook state.
- Mock: `Mock()` replaces the save function and verifies its calls.

## Temporary File Testing

The storage tests use pytest's `tmp_path` fixture to test
saving and loading with real temporary files without changing
the application's actual gradebook data.

# Lab 05 Notes

## Task 1 — Initial Coverage

- Total coverage: 50%
- File with the lowest coverage: `gradebook.py` (35%)
- Test result: 27 passed in 0.39s

## Task 2 — TDD Weight Rule

### Cycle 1 — Empty weights

- Test: `ensure_weight_fits([], 50)`
- Initial failure message: [paste actual failure message]
- Final result: Passed

### Cycle 2 — Total exceeds 100

- Test: `ensure_weight_fits([60], 50)`
- Initial failure message: [paste actual failure message]
- Final result: Passed; raises `ValidationError` containing "100"

### Cycle 3 — Total equals 100

- Test: `ensure_weight_fits([60], 40)`
- Did it fail first? [Yes or No, based on actual result]
- Final result: Passed

### Cycle 4 — Decimal weights

- Test: `ensure_weight_fits([9.3, 27.3, 33.7], 29.7)`
- Initial failure message: [paste actual failure message, or note that it passed initially]
- Final result: Passed with tolerance
