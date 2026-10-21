
from rules import ensure_weight_fits


def test_empty_weights_fit():
    ensure_weight_fits([], 50)


import pytest

from errors import ValidationError
from rules import ensure_weight_fits


def test_empty_weights_fit():
    ensure_weight_fits([], 50)


def test_weight_over_100_is_rejected():
    with pytest.raises(ValidationError, match="100"):
        ensure_weight_fits([60], 50)
