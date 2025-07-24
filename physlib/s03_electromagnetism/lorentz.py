"""Lorentz force calculations.

The Lorentz force law describes the force on a charge ``q`` moving with
velocity ``v`` in electric field ``E`` and magnetic field ``B``:

.. math:: \mathbf{F} = q (\mathbf{E} + \mathbf{v} \times \mathbf{B}).
"""

import numpy as np


def lorentz_force(q: float, e_field: np.ndarray, b_field: np.ndarray, velocity: np.ndarray) -> np.ndarray:
    """Return Lorentz force vector."""
    return q * (e_field + np.cross(velocity, b_field))
