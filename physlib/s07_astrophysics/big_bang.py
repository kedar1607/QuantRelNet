"""Very simplified cosmological expansion calculator.

Assumes a matter-dominated Friedmann universe where the scale factor
evolves as ``a(t) ∝ t^{2/3}``.  ``H0`` is the Hubble constant in km/s/Mpc.
"""

import numpy as np


def scale_factor(t: float, H0: float = 70.0) -> float:
    """Return scale factor ``a(t)`` for cosmic time ``t``."""
    H0_si = H0 * 1000 / (3.0857e22)
    return (3 * H0_si * t / 2) ** (2 / 3)
