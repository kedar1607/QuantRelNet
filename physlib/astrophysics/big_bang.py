"""Very simplified cosmological expansion calculator."""

import numpy as np


def scale_factor(t: float, H0: float = 70.0) -> float:
    """Return scale factor assuming a matter-dominated universe."""
    H0_si = H0 * 1000 / (3.0857e22)
    return (3 * H0_si * t / 2) ** (2 / 3)
