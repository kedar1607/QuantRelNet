"""Heisenberg uncertainty principle calculations."""

import numpy as np


def min_uncertainty(std_x: float) -> float:
    """Return minimum momentum uncertainty given position uncertainty."""
    hbar = 1.054_571_817e-34
    return hbar / (2 * std_x)


def verify_uncertainty(std_x: float, std_p: float) -> bool:
    """Check if given uncertainties satisfy the principle."""
    hbar = 1.054_571_817e-34
    return std_x * std_p >= hbar / 2
