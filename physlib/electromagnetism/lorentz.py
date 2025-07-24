"""Lorentz force calculations."""

import numpy as np


def lorentz_force(q: float, e_field: np.ndarray, b_field: np.ndarray, velocity: np.ndarray) -> np.ndarray:
    """Return Lorentz force F = q(E + v x B)."""
    return q * (e_field + np.cross(velocity, b_field))
