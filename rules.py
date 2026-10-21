
from errors import ValidationError

TOLERANCE = 1e-9


def ensure_weight_fits(existing_weights, new_weight):
    total = sum(existing_weights) + new_weight

    if total > 100 + TOLERANCE:
        raise ValidationError(
            "Total assessment weight cannot exceed 100"
        )
