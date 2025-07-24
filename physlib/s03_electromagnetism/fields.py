"""Simple electromagnetic field representations.

Uses Coulomb's law for the electric field of a point charge:

.. math:: \mathbf{E} = k \frac{q \mathbf{r}}{|\mathbf{r}|^3}

where ``q`` is charge and ``r`` is the displacement from the charge to
the observation point.
"""

import numpy as np


def point_charge_field(q: float, position: np.ndarray, observation: np.ndarray) -> np.ndarray:
    """Return electric field of a point charge."""
    k = 8.9875517923e9
    r = observation - position
    r_mag = np.linalg.norm(r)
    return k * q * r / r_mag**3
