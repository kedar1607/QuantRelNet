"""Heisenberg uncertainty principle calculations.

Heisenberg's principle states that the uncertainties in position
``Δx`` and momentum ``Δp`` satisfy ``Δx Δp ≥ ħ/2``.  The helper functions
check this relation and compute the minimum momentum uncertainty for a
given ``Δx``.
"""

import numpy as np


def min_uncertainty(std_x: float) -> float:
    """Return minimum momentum uncertainty given ``Δx``."""
    hbar = 1.054_571_817e-34
    return hbar / (2 * std_x)


def verify_uncertainty(std_x: float, std_p: float) -> bool:
    """Check whether ``Δx Δp ≥ ħ/2`` is satisfied."""
    hbar = 1.054_571_817e-34
    return std_x * std_p >= hbar / 2
