from errors import ValidationError


def ensure_weight_fits(existing_weights, new_weight):
    total = sum(existing_weights) + new_weight

    if total > 100:
        raise ValidationError("Total assessment weight cannot exceed 100")
