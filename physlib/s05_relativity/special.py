"""Special relativity utilities.

Based on Einstein's theory of special relativity.  The Lorentz factor is
``γ = 1/√(1 - v^2/c^2)``.  Time dilation and length contraction follow
directly from this factor.
"""

import numpy as np

c = 299_792_458.0


def time_dilation(proper_time: float, velocity: float) -> float:
    """Return dilated time ``t = γ τ`` from proper time ``τ``."""
    gamma = 1 / np.sqrt(1 - (velocity / c) ** 2)
    return gamma * proper_time


def length_contraction(proper_length: float, velocity: float) -> float:
    """Return contracted length ``L = L_0/γ``."""
    gamma = 1 / np.sqrt(1 - (velocity / c) ** 2)
    return proper_length / gamma
