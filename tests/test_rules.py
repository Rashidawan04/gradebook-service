
from rules import ensure_weight_fits


def test_empty_weights_fit():
    ensure_weight_fits([], 50)
