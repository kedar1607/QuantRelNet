"""Quantum tunneling utilities.

Computes the transmission probability for a particle with energy
``E`` encountering a rectangular potential barrier of height
``V_0`` and width ``L`` using the WKB approximation.
"""

import numpy as np


def barrier_transmission(energy: float, barrier_height: float, width: float, mass: float) -> float:
    """Return transmission probability for a square potential barrier."""
    hbar = 1.054_571_817e-34
    kappa = np.sqrt(2 * mass * (barrier_height - energy)) / hbar
    return np.exp(-2 * kappa * width)
