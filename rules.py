
from collections.abc import Sequence

from errors import ValidationError

MAX_TOTAL_WEIGHT: float = 100.0
TOLERANCE: float = 1e-9


def ensure_weight_fits(
    existing_weights: Sequence[float],
    new_weight: float,
) -> None:
    """Ensure the new assessment weight keeps the total within the limit."""
    total = sum(existing_weights) + new_weight

    if total > MAX_TOTAL_WEIGHT + TOLERANCE:
        raise ValidationError(
            f"Total assessment weight cannot exceed {MAX_TOTAL_WEIGHT:g}"
        )
