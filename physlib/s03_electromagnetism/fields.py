"""Simple electromagnetic field representations."""

import numpy as np


def point_charge_field(q: float, position: np.ndarray, observation: np.ndarray) -> np.ndarray:
    """Return electric field from a point charge."""
    k = 8.9875517923e9
    r = observation - position
    r_mag = np.linalg.norm(r)
    return k * q * r / r_mag**3
